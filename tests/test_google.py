from playwright.sync_api import Page, expect


def test_google_homepage(page: Page):
    page.goto("https://www.google.com")
    expect(page).to_have_title("Google")