from contextlib import contextmanager
from pathlib import Path
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
                "--server.runOnSave",
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

    Path("example_app/example_one.py").write_text(
        """import streamlit as st
from st_pages import add_page_title

add_page_title(layout="wide")

st.write("This is just a sample page!")
"""
    )


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")

    yield

    TEST_TEXT = "THIS IS A TEST"

    current_text = Path("example_app/example_one.py").read_text()

    with Path("example_app/example_one.py").open("w") as f:
        f.write(current_text.replace(f"\nst.write('{TEST_TEXT}')\n", ""))


def test_page_update(page: Page):
    TEST_TEXT = "THIS IS A TEST"
    page.get_by_role("link", name="Example One").click()

    expect(page).to_have_title("Example One")

    page.screenshot(path="screenshot-edits0.png", full_page=True)

    try:
        expect(page.get_by_text(TEST_TEXT)).not_to_be_visible()
    except Exception as e:
        page.screenshot(path="screenshot-edits1.png", full_page=True)
        raise e

    with Path("example_app/example_one.py").open("a") as f:
        f.write(f"\nst.write('{TEST_TEXT}')\n")

    try:
        expect(page.get_by_text(TEST_TEXT)).to_be_visible()
    except Exception as e:
        page.screenshot(path="screenshot-edits2.png", full_page=True)
        raise e
