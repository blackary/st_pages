from pathlib import Path

import streamlit as st

with st.echo("below"):
    from st_pages import Page, Section, add_page_title, show_pages

    "## Declaring the pages in your app:"

    show_pages(
        [
            Page("demo_st_page.py", "主页", "🏠"),
            # Can use :<icon-name>: or the actual icon
            Page("pages/page_1.py", "第一页", ":books:"),

            # Since this is a Section, all the pages underneath it will be indented
            # The section itself will look like a normal page, but it won't be clickable
            Section(name="Cool apps", icon=":pig:"),
            # The pages appear in the order you pass them
            Page("pages/page_4.py", "Page 四", "📖"),
            Page("pages/page_2.py", "Page 二", "✏️"),

            Section(name="Other apps", icon=":horse:"),
            # Will use the default icon and name based on the filename if you don't pass them
            Page("pages/page_3.py"),

            # You can also pass in_section=False to a page to make it un-indented
            Page("pages/page_5.py", "Page 五", "🧰", in_section=False),
        ]
    )

    add_page_title()  # Optional method to add title and icon to current page
    # Also calls add_indentation() by default, which indents pages within a section

TOML_CONFIG = ".streamlit/pages_sections.toml"
if Path(TOML_CONFIG).exists():

    "## Alternative approach, using a config file"

    "Contents of `.streamlit/pages_sections.toml`"

    st.code(Path(TOML_CONFIG).read_text(), language="toml")

    "Streamlit script:"

    with st.echo("below"):
        from st_pages import show_pages_from_config

        show_pages_from_config(TOML_CONFIG)

    "See more at https://github.com/blackary/st_pages"


with st.expander("Show documentation"):
    from st_pages import add_indentation

    st.help(show_pages)

    st.help(Page)

    st.help(add_page_title)

    st.help(Section)

    st.help(add_indentation)
