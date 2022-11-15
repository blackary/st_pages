import streamlit as st

"# A Better way to Set Up Multi-Page Streamlit Apps"

with st.echo("above"):
    from st_pages import Page, show_pages

    show_pages(
        [
            Page("example_app/streamlit_app.py", "Home", "🏠"),
            Page(
                "example_app/example_one.py", "Example One", ":books:"
            ),  # Can use :<icon-name>: or the actual icon
            Page(
                "example_app/example_four.py", "Example Four", "📖"
            ),  # The pages appear in the order you pass them
            Page("example_app/example_two.py", "Example Two", "✏️"),
            Page(
                "example_app/example_three.py"
            ),  # Will use the default icon and name based on the page name
        ]
    )
