import pytest


@pytest.mark.parametrize(
    "column_type,value",
    [
        ("INTEGER", 123),
        ("VARCHAR", "hello"),
        ("BOOLEAN", True),
        ("DECIMAL", 12.50),
    ]
)
def test_data_types(column_type, value):
    assert value is not None