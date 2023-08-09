"""Page for modifying bot prompts."""
import streamlit as st
from backend_controller import create_new_prompt, get_prompt
from utils import query_params


def render_prompt() -> None:
    """Page for modifying bot prompts."""
    current_bot = query_params.get_form_url("bot_id")
    current_prompt = get_prompt(current_bot)

    st.title("Main Bot prompt")
    prompt = st.text_area("", value=current_prompt, label_visibility="collapsed")
    st.button(
        "Save",
        on_click=create_new_prompt,
        args=([prompt, current_bot]),
        disabled=prompt == current_prompt,
    )
