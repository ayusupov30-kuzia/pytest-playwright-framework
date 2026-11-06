import pytest
from playwright.sync_api import expect

def test_successful_login(login_page, valid_credentials):

    login_page.login(
        valid_credentials["username"],
        valid_credentials["password"]
    )

    expect(login_page.message).to_contain_text(
        "You logged into a secure area!"
    )

@pytest.mark.parametrize(
    "username,password,expected_message",
    [
        (
            "invalid_user",
            "wrong_password",
            "Your username is invalid!"
        ),
        (
            "tomsmith",
            "wrong_password",
            "Your password is invalid!"
        ),
        (
            "",
            "",
            "Your username is invalid!"
        ),
    ]
)
def test_invalid_login_scenarios(
    login_page,
    username,
    password,
    expected_message
):

    login_page.login(username, password)

    expect(login_page.message).to_contain_text(
        expected_message
    )


def test_credentials_available(valid_credentials):
    assert valid_credentials["username"] == "tomsmith"