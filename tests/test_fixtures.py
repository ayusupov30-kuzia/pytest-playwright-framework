import pytest

@pytest.fixture
def user():
    print("\nCreating test user")

    return {
        "name": "Alex",
        "roles": "QA Lead",
        "active": True
    }

def test_user_name(user):
    assert user["name"] == "Alex"
def test_user_roles(user):
    assert user["roles"] == "QA Lead"
def test_user_active(user):
    assert user["active"] is True