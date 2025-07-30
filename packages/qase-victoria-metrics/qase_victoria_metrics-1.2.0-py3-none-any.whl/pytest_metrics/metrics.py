"""
This module provides functionality to collect and report test execution results
to Qase TestOps and VictoriaMetrics.

It extracts test metadata, formats the results, and sends them to VictoriaMetrics
for further analysis in a Prometheus-compatible format.
"""

import json
import os
import time
import sys
from typing import Dict, Any, List, Optional
import logging
import requests
from _pytest.reports import TestReport
from _pytest.nodes import Item
from concurrent.futures import ThreadPoolExecutor, as_completed

# Environment variables
VICTORIA_URL: Optional[str] = os.environ.get("VICTORIA_URL")
VICTORIA_URL_1: Optional[str] = os.environ.get("VICTORIA_URL_1")
RUN_ID: Optional[str] = os.environ.get("QASE_TESTOPS_RUN_ID")
PROJECT: Optional[str] = os.environ.get("QASE_TESTOPS_PROJECT")
PLATFORM: Optional[str] = os.environ.get("PLATFORM")
QASE_TOKEN: Optional[str] = os.environ.get("QASE_TESTOPS_API_TOKEN")
ADMIN_TOKEN: Optional[str] = os.environ.get("QASE_ADMIN_TOKEN")
PUSH_TO_VICTORIA: Optional[str] = os.environ.get("PUSH_TO_VICTORIA")
MULTIPLE_REPORT: Optional[str] = os.environ.get("MULTIPLE_REPORT")
DELETE_TEMP_FILE: Optional[str] = os.environ.get("DELETE_TEMP_FILE")
PILLAR: Optional[str] = os.environ.get("PILLAR")


class MetricsReport:
    """
    A class for collecting and reporting test execution results to Qase TestOps
    and VictoriaMetrics.

    Attributes:
        run_id (Optional[str]): The test run ID from Qase TestOps.
        platform (Optional[str]): The test execution platform.
        results (List[Dict[str, Any]]): Collected test results.
    """

    def __init__(
        self, run_id: Optional[str] = RUN_ID, platform: Optional[str] = PLATFORM
    ) -> None:
        """
        Initializes the MetricsReport instance.

        Args:
            run_id (Optional[str]): The test run ID from Qase TestOps.
            platform (Optional[str]): The test execution platform.
        """
        self.run_id: Optional[str] = run_id
        self.platform: Optional[str] = platform
        self.results: List[Dict[str, Any]] = []
        self.multiplecase: List[Dict[str, Any]] = []

    def collect_result(
        self, item: Item, report: TestReport, status: str = None
    ) -> None:
        """
        Collects test execution results and stores them in `results`.

        Args:
            item (Item): The pytest test item.
            report (TestReport): The test execution report.
        """
        if report.when == "call" or (report.when == "setup" and report.failed):

            case_id = getattr(item.function, "__custom_id_suite__", None)
            suite_title = getattr(item.function, "__custom_qase_suite__", None)
            case_title = getattr(item.function, "__custom_qase_title__", None)
            tags = getattr(item.function, "__custom_qase_tags__", None)

            # Ensure attributes are always lists
            if not isinstance(suite_title, list):
                suite_title = (
                    [suite_title]
                    if suite_title is not None
                    else ["UNKNOWN SUITE TITLE"]
                )
            if not isinstance(case_id, list):
                case_id = [case_id] if case_id is not None else ["UNKNOWN CASE ID"]
            if not isinstance(case_title, list):
                case_title = (
                    [case_title]
                    if case_title is not None
                    else ["UNKNOWN TESTCASE TITLE"]
                )

            duration = int(report.duration * 1000)
            error_message = None
            stacktrace = None

            status = status if status else report.outcome
            if status in ["failed", "error"]:
                error_message = report.longreprtext.split("\n")[-1]
                stacktrace = report.longreprtext

            max_length = max(len(case_id), len(case_title))

            for i in range(max_length):
                self.multiplecase.append(
                    {
                        "id": (case_id[i] if i < len(case_id) else case_id[-1]),
                        "title": (
                            case_title[i] if i < len(case_title) else case_title[-1]
                        ),
                    }
                )

                self.results.append(
                    {
                        "run_id": self.run_id,
                        "case_id": (case_id[i] if i < len(case_id) else case_id[-1]),
                        "title": (
                            case_title[i] if i < len(case_title) else case_title[-1]
                        ),
                        "suite_title": (
                            suite_title[i] if i < len(suite_title) else suite_title[-1]
                        ),
                        "status": status,
                        "time_spent_ms": duration,
                        "error": error_message,
                        "stacktrace": stacktrace,
                        "tags": tags,
                        "platform": self.platform,
                    }
                )

    def save_to_temp_file(self, worker_id: str) -> None:
        """
        Save worker results to a temporary JSON file.

        Args:
            worker_id (str): The ID of the worker process.
        """
        if not self.results:
            return  # Avoid writing empty files
        filename = (
            f"{PILLAR}_pytest_worker_{worker_id}.json"
            if MULTIPLE_REPORT in [None, "true"]
            else f"pytest_worker_{worker_id}.json"
        )
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f)

        mapping_name = (
            f"{PILLAR}_qase_mappings_{worker_id}.json"
            if MULTIPLE_REPORT in [None, "true"]
            else f"_qase_mappings_{worker_id}.json"
        )
        with open(mapping_name, "w", encoding="utf-8") as f:
            json.dump(self.multiplecase, f)

    def load_and_merge_results(self) -> None:
        """
        Load results from temporary worker files and merge them into `results`.
        """
        # Save multiple list qase id here
        mapping_name = "qase_mappings.json"
        with open(mapping_name, "w", encoding="utf-8") as f:
            json.dump(self.multiplecase, f)

        for file in os.listdir():
            if "pytest_worker_" in file and file.endswith(".json"):
                with open(file, "r", encoding="utf-8") as f:
                    worker_data = json.load(f)
                    if worker_data:
                        self.results.extend(worker_data)
                if DELETE_TEMP_FILE in [None, "true"]:
                    os.remove(file)

            if "_qase_mappings_" in file and file.endswith(".json"):
                with open(file, "r", encoding="utf-8") as f:
                    worker_data = json.load(f)
                    if worker_data:
                        self.multiplecase.extend(worker_data)

    def sanitize_result(self) -> None:
        """
        Sanitizes `self.results` to keep only the latest test result per `case_id`.

        If a `case_id` has multiple results with different statuses, the latest "passed"
        result is prioritized over failed ones.

        Returns:
            None: Updates `self.results` in place.
        """
        latest_result: Dict[int, Dict[str, object]] = {}

        for result in self.results:
            case_id = result["case_id"]
            if case_id not in latest_result or result["status"] == "passed":
                latest_result[case_id] = result

        self.results = list(latest_result.values())

    def update_list_titles(self, id, title):
        url = f"https://api.qase.io/v1/case/{PROJECT}/{id}"

        payload = {"title": title}
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "Token": ADMIN_TOKEN,
        }

        try:
            response = requests.patch(url, json=payload, headers=headers, timeout=30)
        except requests.RequestException as e:
            print(f"[{id}] ERROR: {e}")

    def run_parallel_updates(self, multiplecase, max_workers=10):
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [
                executor.submit(self.update_list_titles, item["id"], item["title"])
                for item in multiplecase
            ]
            for future in as_completed(futures):
                future.result()

    def send_to_victoria_metrics(self) -> Optional[requests.Response]:
        """
        Sends collected test results to VictoriaMetrics in Prometheus format.

        Returns:
            Optional[requests.Response]: The response from the VictoriaMetrics API,
            or None if an error occurred.
        """
        if not self.results:
            print("No test results to send.")
            return None

        # Update multiple case title
        time.sleep(3)
        self.run_parallel_updates(self.multiplecase)

        self.sanitize_result()

        metrics: List[str] = []
        timestamp = int(time.time())
        push_date = int(time.time() * 1000)

        def format_labels(result: Dict[str, Any]) -> str:
            """
            Formats test case metadata into a Prometheus-compatible label string.

            Args:
                result (Dict[str, Any]): The test execution result dictionary.

            Returns:
                str: A formatted string for Prometheus labels.
            """
            return (
                f'run_id="{result["run_id"]}", '
                f'suite_title="{result["suite_title"]}", '
                f'status="{result["status"]}", push_date="{push_date}", '
                f'title="{result["title"]}", tags="{result["tags"]}", '
                f'platform="{result["platform"]}", case_id="{result["case_id"]}"'
            )

        for result in self.results:
            status_value = "0" if result["status"] == "failed" else "1"
            error_message = result["error"] if result["error"] else "None"
            labels = format_labels(result)

            metrics.append(
                f'test_case_duration_ms{{{labels}}} {result["time_spent_ms"]} {timestamp}'
            )
            metrics.append(f"test_case_status{{{labels}}} {status_value} {timestamp}")

            if result["status"] == "failed":
                failure_labels = f'{labels}, error_message="{error_message}"'
                metrics.append(f"test_case_failures{{{failure_labels}}} 1 {timestamp}")

        payload = "\n".join(metrics)

        if PUSH_TO_VICTORIA == "true":
            try:
                response = requests.post(
                    VICTORIA_URL,
                    data=payload,
                    headers={"Content-Type": "text/plain"},
                    timeout=300,
                )
                print(
                    f"Response status code: {response.status_code}\n Response text : {response.text}"
                )
                response.raise_for_status()
            except requests.exceptions.RequestException as e:
                print(f"Error sending data to VictoriaMetrics: {e}")
                sys.exit(1)
                return None

            if VICTORIA_URL_1:
                try:
                    response_1 = requests.post(
                        VICTORIA_URL_1,
                        data=payload,
                        headers={"Content-Type": "text/plain"},
                        timeout=300,
                    )
                    print(
                        f"Response 1 status code: {response_1.status_code}\n Response 1 text : {response_1.text}"
                    )
                    response_1.raise_for_status()
                except requests.exceptions.RequestException as e:
                    print(f"Error sending data to VictoriaMetrics URL 1: {e}")
                    sys.exit(1)
                    return None

            print("\nData pushed successfully to Victoria Metrics\n")
            return response
        else:
            worker_id = os.getenv("PYTEST_XDIST_WORKER")

            if not worker_id:
                filename = f"{PLATFORM}_pytest_worker_{PILLAR}.json"
                filepath = os.path.abspath(filename)

                print(f"Data to write: {self.results}", self.results)

                try:
                    with open(filepath, "w", encoding="utf-8") as f:
                        json.dump(self.results, f)
                    print(f"File successfully written at: {filepath}")
                except Exception as e:
                    print(f"Error writing file: {e}")

            print("Sending Metrics to Victoria is Disabled")
