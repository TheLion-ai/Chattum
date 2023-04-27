import streamlit as st
from components.tools import RequestsTool

st.title("Tools")

tools_bar, tools_content = st.columns([1,3])

with tools_bar:
    st.button("Add Tool")
    
with tools_content:
    tool = RequestsTool()
    tool.render()
    