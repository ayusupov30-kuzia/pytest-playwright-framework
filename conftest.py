
import pytest

from playwright.sync_api import Page
from pages.login_page import LoginPage


pytest_plugins = ["reporting.reporter"]


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.navigate()
    return login


@pytest.fixture(scope="session")
def valid_credentials():
    print("\nLoading valid credentials")

    return {
        "username": "tomsmith",
        "password": "SuperSecretPassword!",
    }
