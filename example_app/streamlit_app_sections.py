import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

nav = get_nav_from_toml(".streamlit/pages_sections.toml")

st.logo("logo.png")

pg = st.navigation(nav)

add_page_title(pg, layout="wide")

pg.run()

st.stop()
