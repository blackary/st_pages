def test_import():
    from st_pages import Page, add_page_title, show_pages  # noqa: F401


def test_page():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py")
    assert page.page_name == "Test Streamlit Pages"
    assert page.page_icon == ""
    assert page.page_hash == "556b734b62fe8a1721eca82f9f6bea28"


def test_page_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert page.page_icon == "🐶"
