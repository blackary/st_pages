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
    assert page.icon is None


def test_page_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":dog:")
    assert page.icon == "🐶"


def test_material_icon():
    from st_pages import Page

    page = Page("tests/test_streamlit_pages.py", icon=":material/refresh:")
    assert page.icon == ":material/refresh:"


def test_unknown_shortcode_is_preserved():
    from st_pages import translate_icon

    # An unrecognized shortcode must keep its colons rather than being
    # silently reduced to a colon-stripped fragment. Streamlit validates
    # icons downstream, and preserving the original input keeps its error
    # message (and the value stored on the page) faithful to what the user
    # actually passed in.
    assert translate_icon(":this_is_not_an_emoji:") == ":this_is_not_an_emoji:"


def test_known_shortcode_still_translates():
    from st_pages import translate_icon

    assert translate_icon(":dog:") == "🐶"
