def test_import():
    from st_pages import (  # noqa: F401
        Page,
        Section,
        add_indentation,
        add_page_title,
        show_pages,
        show_pages_from_config,
    )


def test_page():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py")
    assert page.page_name == "Test Streamlit Pages"
    assert page.page_icon == ""


def test_page_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert page.page_icon == "🐶"
