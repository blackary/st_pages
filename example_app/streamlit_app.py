from pathlib import Path

import streamlit as st

with st.echo("below"):
    from st_pages import Page, add_page_title, show_pages

    "## Declaring the pages in your app:"

    show_pages(
        [
            Page("example_app/streamlit_app.py", "Home", "🏠"),
            # Can use :<icon-name>: or the actual icon
            Page("example_app/example_one.py", "Example One", ":books:"),
            # The pages appear in the order you pass them
            Page("example_app/example_four.py", "Example Four", "📖"),
            Page("example_app/example_two.py", "Example Two", "✏️"),
            # Will use the default icon and name based on the filename if you don't
            # pass them
            Page("example_app/example_three.py"),
            Page("example_app/example_five.py", "Example Five", "🧰"),
        ]
    )

    add_page_title()  # Optional method to add title and icon to current page

"## Alternative approach, using a config file"

"Contents of `.streamlit/pages.toml`"

st.code(Path(".streamlit/pages.toml").read_text(), language="toml")

"Streamlit script:"

with st.echo("below"):
    from st_pages import show_pages_from_config

    show_pages_from_config()

"See more at https://github.com/blackary/st_pages"

with st.expander("Show documentation"):
    st.help(show_pages)

    st.help(Page)

    st.help(add_page_title)
