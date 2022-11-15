import streamlit as st

from st_pages import Page, show_pages

"# A Better way to Set Up Multi-Page Streamlit Apps"

with st.echo("above"):
    show_pages(
        [
            Page("streamlit_app.py", "Home", "🏠"),
            Page(
                "example_one.py", "Example One", ":books:"
            ),  # Can use :icon: or "the actual icon"
            Page("example_four.py", "Example Four", "📖"),  # The order matters
            Page("example_two.py", "Example Two", "✏️"),
            Page("example_three.py"),  # Will use the default icon and name
        ]
    )
