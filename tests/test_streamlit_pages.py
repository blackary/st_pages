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
    assert page.name == "test_streamlit_pages"
    assert page.icon == ""


def test_page_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert page.icon == "🐶"


def test_material_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":material/refresh:")
    assert page.icon == ":material/refresh:"
