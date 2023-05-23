"""Page for modifying bot prompts."""
import streamlit as st
from backend_controller import create_new_prompt
from components.sidebar import sidebar_controller

st.session_state.current_bot = st.session_state.get("current_bot", None)
sidebar_controller()

st.title("Chattum")
st.text("Main Bot prompt")
st.text(st.session_state.current_bot)
prompt = st.text_area("")
bot_id = st.session_state.current_bot
st.button("Save", on_click=create_new_prompt, args=([prompt, bot_id]))
