import streamlit as st
from st_pages import add_page_title

add_page_title()

with st.sidebar:
    # st.write("sidebar")
    st.radio( "Choose option",  ["Option 1", "Option 2"],  index=0, key="page3_radio")

st.write("This is Page 3 with sidebar")

option = st.session_state.get("page3_radio")

st.write(f"Your selection is {option}")