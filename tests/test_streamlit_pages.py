def test_import():
    from streamlit_pages import Page, show_pages


def test_page():
    from streamlit_pages import Page

    page = Page("tests/test_streamlit_pages.py")
    assert page.page_name == "Test Streamlit Pages"
    assert page.page_icon == ""
    assert page.page_hash == "556b734b62fe8a1721eca82f9f6bea28"


def test_page_icon():
    from streamlit_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert page.page_icon == "🐶"
