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
def before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")


def test_pages_available(page: Page):
    expect(page.get_by_text("🏠 Home")).to_be_visible()

    page.get_by_role("link", name="Example One").click()

    expect(page).to_have_title("Example One")


def test_deprecation_warning(page: Page):
    expect(
        page.get_by_text("st.experimental_singleton is deprecated")
    ).not_to_be_visible()


def test_wide_mode(page: Page):
    """
    Make sure that the wide mode argument is working by comparing the x positions of the
    "Example One" and "Example Two" headers. The "Example Two" header should be further
    to the right than the "Example One" header. Currently it is 50px further to the
    right, but 30 should be enough to catch any regressions.
    """
    page.get_by_role("link", name="Example One").click()

    bbox = page.get_by_text("📚 Example One").bounding_box()

    assert bbox is not None

    wide_mode_x = bbox["x"]

    page.get_by_role("link", name="Example Two").click()

    bbox = page.get_by_text("✏️ Example Two").bounding_box()

    assert bbox is not None

    regular_x = bbox["x"]

    assert (regular_x - wide_mode_x) > 30
