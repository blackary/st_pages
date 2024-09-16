import streamlit as st

from st_pages import hide_pages

st.write("This is just a sample page!")

options = ["Show all pages", "Hide pages 2 and 3", "Hide Other apps Section"]

if (
    "_pages_hidden" in st.session_state
    or "hide_pages_selection" not in st.session_state
):
    selection = st.radio("Test page hiding", options, key="_pages_hidden")
else:
    index = options.index(st.session_state["hide_pages_selection"])
    selection = st.radio("Test page hiding", options, index=index, key="_pages_hidden")

if selection == "Show all pages":
    hide_pages([])
elif selection == "Hide pages 2 and 3":
    hide_pages(["Example Two", "example three"])
elif selection == "Hide Other apps Section":
    hide_pages(["Other apps"])

st.session_state["hide_pages_selection"] = selection

st.write(
    "See another dynamic page example in the Streamlit docs [here](https://docs.streamlit.io/develop/tutorials/multipage/dynamic-navigation)"
)
