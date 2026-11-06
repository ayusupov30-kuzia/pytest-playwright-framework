
import json
from pathlib import Path

import pytest


def classify_test_status(failures):
    if any(failure["phase"] == "call" for failure in failures):
        return "failed"

    if any(
        failure["phase"] in ("setup", "teardown")
        for failure in failures
    ):
        return "error"

    return "passed"


def calculate_summary(tests):
    summary = {
        "total": len(tests),
        "passed": 0,
        "failed": 0,
        "error": 0,
        "skipped": 0,
        "setup_failures": 0,
        "call_failures": 0,
        "teardown_failures": 0,
    }

    for test in tests:
        status = test["status"]

        if status in ("passed", "failed", "error", "skipped"):
            summary[status] += 1

        for failure in test["failures"]:
            key = f"{failure['phase']}_failures"

            if key in summary:
                summary[key] += 1

    assert summary["total"] == (
        summary["passed"]
        + summary["failed"]
        + summary["error"]
        + summary["skipped"]
    ), "Summary counts do not match total tests"

    return summary


def pytest_configure(config):
    config.test_results = {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    test_id = item.nodeid
    results = item.config.test_results

    if test_id not in results:
        results[test_id] = {
            "name": test_id,
            "status": "passed",
            "duration": 0.0,
            "failures": [],
        }

    test_result = results[test_id]
    test_result["duration"] += report.duration

    if report.failed:
        test_result["failures"].append({
            "phase": report.when,
            "error_type": (
                call.excinfo.typename
                if call.excinfo is not None
                else None
            ),
            "message": report.longreprtext,
        })

        test_result["status"] = classify_test_status(
            test_result["failures"]
        )

    elif report.skipped and not test_result["failures"]:
        test_result["status"] = "skipped"


def pytest_sessionfinish(session, exitstatus):
    tests = list(session.config.test_results.values())

    for test in tests:
        test["duration"] = round(test["duration"], 3)

    report_data = {
        "summary": calculate_summary(tests),
        "tests": tests,
    }

    report_path = Path("test-results/report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    report_path.write_text(
        json.dumps(report_data, indent=2),
        encoding="utf-8",
    )

    print(f"\nJSON report generated: {report_path}")


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    tests = list(config.test_results.values())
    summary = calculate_summary(tests)

    terminalreporter.write_sep(
        "=",
        "CUSTOM TEST EXECUTION SUMMARY",
    )

    for key, value in summary.items():
        terminalreporter.write_line(f"{key}: {value}")
