import streamlit as st
from st_pages import add_page_title, hide_pages

add_page_title()

st.write("This is just a sample page!")

selection = st.radio(
    "Test page hiding",
    ["Show all pages", "Hide pages 1 and 2", "Hide Other apps Section"],
)

if selection == "Show all pages":
    hide_pages([])
elif selection == "Hide pages 1 and 2":
    hide_pages(["Example One", "Example Two"])
elif selection == "Hide Other apps Section":
    hide_pages(["Other apps"])

st.selectbox("test_select", options=["1", "2", "3"])
