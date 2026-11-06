
import json
import shutil
from pathlib import Path

pytest_plugins = ["pytester"]


def test_json_reporter(pytester):
    project_root = Path(__file__).resolve().parents[1]

    # Copy only the reporting package.
    shutil.copytree(
        project_root / "reporting",
        pytester.path / "reporting",
    )

    # Register the reporting plugin in the temporary project.
    pytester.makeconftest(
        'pytest_plugins = ["reporting.reporter"]'
    )

    pytester.makepyfile(
        test_scenarios="""
import pytest


def test_success():
    assert 1 == 1


def test_assertion_failure():
    assert 1 == 2


@pytest.fixture
def broken_setup():
    raise RuntimeError("Database unavailable")


def test_setup_error(broken_setup):
    assert True


@pytest.fixture
def broken_teardown():
    yield
    raise RuntimeError("Cleanup failed")


def test_double_failure(broken_teardown):
    assert 1 == 2, "Assertion failed"
"""
    )

    result = pytester.runpytest(
        "-v",
        "-p", "no:playwright",
    )

    # Pytest counts phase reports, not unique test records.
    result.assert_outcomes(
        passed=1,
        failed=2,
        errors=2,
    )

    report_path = pytester.path / "test-results" / "report.json"

    assert report_path.exists()

    report = json.loads(
        report_path.read_text(encoding="utf-8")
    )

    summary = report["summary"]

    assert summary["total"] == 4
    assert summary["passed"] == 1
    assert summary["failed"] == 2
    assert summary["error"] == 1
    assert summary["skipped"] == 0

    assert summary["setup_failures"] == 1
    assert summary["call_failures"] == 2
    assert summary["teardown_failures"] == 1

    tests = report["tests"]

    assert len(tests) == 4
    assert len({test["name"] for test in tests}) == 4

    double_failure = next(
        test for test in tests
        if "test_double_failure" in test["name"]
    )

    assert double_failure["status"] == "failed"
    assert len(double_failure["failures"]) == 2

    phases = {
        failure["phase"]
        for failure in double_failure["failures"]
    }

    assert phases == {"call", "teardown"}

    error_types = {
        failure["phase"]: failure["error_type"]
        for failure in double_failure["failures"]
    }

    assert error_types == {
        "call": "AssertionError",
        "teardown": "RuntimeError"
    }    
