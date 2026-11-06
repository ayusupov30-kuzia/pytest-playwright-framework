import pytest

@pytest.fixture
def failing_setup():
    print("\n***** Running setup")
    raise RuntimeError("Intentional setup failure")
    yield


@pytest.fixture
def failing_teardown():
    print("\n***** Running setup")
    yield
    print("\n***** Running teardown")
    raise RuntimeError("Intentional teardown failure")

@pytest.fixture
def failing_call_and_teardown():
    print("\n***** Running setup")
    yield
    print("\n***** Running teardown")
    raise RuntimeError("Intentional teardown failure")


def test_setup_failure(failing_setup):
    print("This should NEVER execute")


def test_teardown_failure(failing_teardown):
    print("Test body executes successfully")
    assert True

def test_call_and_teardown_failure(failing_call_and_teardown):
    print("\n***** Running test body")
    assert 1 == 2, "Intentional call failure"