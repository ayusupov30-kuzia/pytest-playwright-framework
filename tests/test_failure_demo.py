from playwright.sync_api import Page, expect


def test_failure_screenshot(page: Page):
    page.goto("https://the-internet.herokuapp.com/login")

    expect(page.locator("h2")).to_have_text(
        "This title is intentionally incorrect"
    )