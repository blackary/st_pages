def test_import():
    from st_pages import (  # noqa: F401
        Page,
        Section,
        add_page_title,
        get_nav_from_toml,
    )


def test_page():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py")
    assert page.name == "Test Streamlit Pages"
    assert page.icon == ""


def test_page_icon():
    from st_pages import Page, translate_icon

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert translate_icon(page.icon) == "🐶"
