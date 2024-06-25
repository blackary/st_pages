from pathlib import Path

import streamlit as st
from st_pages import add_page_title, get_nav_from_toml

st.write("`streamlit_app.py` contents:")
code = Path("example_app/streamlit_app_sections.py").read_text()

st.code(code, language="python")

st.write("`pages_sections.toml` contents:")
toml_code = Path(".streamlit/pages_sections.toml").read_text()
st.code(toml_code, language="toml")

st.help(get_nav_from_toml)
st.help(add_page_title)
