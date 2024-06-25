from contextlib import contextmanager
from time import sleep

import pytest
from playwright.sync_api import Page, expect

LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@contextmanager
def run_streamlit():
    """Run the streamlit app at examples/streamlit_app.py on port 8599"""
    import subprocess

    if LOCAL_TEST:
        try:
            yield 1
        finally:
            pass
    else:
        p = subprocess.Popen(
            [
                "streamlit",
                "run",
                "example_app/streamlit_app.py",
                "--server.port",
                PORT,
                "--server.headless",
                "true",
            ]
        )

        sleep(5)

        try:
            yield 1
        finally:
            p.kill()


@pytest.fixture(scope="module", autouse=True)
def _before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(autouse=True)
def _before_test(page: Page):
    page.goto(f"localhost:{PORT}")
    # Toggle off sections mode
    page.get_by_test_id("stCheckbox").locator("div").nth(1).click()


def test_pages_available(page: Page):
    expect(page.get_by_text("📄 st-pages")).to_be_visible()

    page.get_by_role("link", name="Example Two").click()

    expect(page).to_have_title("Example Two")


def test_deprecation_warning(page: Page):
    expect(
        page.get_by_text("st.experimental_singleton is deprecated")
    ).not_to_be_visible()


def test_page_hiding(page: Page):
    page.get_by_role("link", name="Try hiding pages").click()

    expect(page.get_by_role("link", name="example three")).to_be_visible()
    expect(page.get_by_role("link", name="Example Five")).to_be_visible()
    page.get_by_text("Hide pages 2 and").click()
    expect(page.get_by_role("link", name="Example two")).not_to_be_visible()
    expect(page.get_by_role("link", name="example three")).not_to_be_visible()
    expect(page.get_by_role("link", name="Example Five")).to_be_visible()

    # Make sure the change is permanent
    page.get_by_role("link", name="st-pages").click()
    expect(page.get_by_role("link", name="Example two")).not_to_be_visible()
    expect(page.get_by_role("link", name="example three")).not_to_be_visible()
    expect(page.get_by_role("link", name="Example Five")).to_be_visible()

    # Make sure the change can be undone
    page.get_by_role("link", name="Try hiding pages").click()
    page.get_by_text("Show all pages").click()
    expect(page.get_by_role("link", name="example three")).to_be_visible()
    expect(page.get_by_role("link", name="Example Five")).to_be_visible()
