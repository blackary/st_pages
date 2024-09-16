from pathlib import Path

import streamlit as st

from st_pages import add_page_title, get_nav_from_toml

st.write("`streamlit_app.py` contents:")
code = Path("example_app/streamlit_app.py").read_text()

st.code(code, language="python")

location = "pages_sections.toml" if st.session_state["use_sections"] else "pages.toml"
st.write(f"`{location}` contents:")
toml_code = Path(f".streamlit/{location}").read_text()
st.code(toml_code, language="toml")

st.help(get_nav_from_toml)
st.help(add_page_title)
