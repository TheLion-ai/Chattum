"""Page for modifying bot prompts."""
import streamlit as st
from backend_controller import create_new_prompt, get_prompt

st.session_state.current_bot = st.experimental_get_query_params()["bot_id"][0]
bot_id = st.session_state.current_bot
current_prompt = get_prompt(bot_id)

st.title("Main Bot prompt")
prompt = st.text_area("", value=current_prompt, label_visibility="collapsed")
st.button(
    "Save",
    on_click=create_new_prompt,
    args=([prompt, bot_id]),
    disabled=prompt == current_prompt,
)
