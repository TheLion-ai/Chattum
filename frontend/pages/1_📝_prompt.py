"""Page for modifying bot prompts."""

import streamlit as st
from backend_controller import create_new_prompt, get_prompt
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
from components.authentication import protect_page

st.set_page_config(
    page_title="Prompt | Chattum",
    page_icon="📝",
)


bot_id = query_params.get_from_url_or_state("bot_id")

ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()

current_prompt = get_prompt(bot_id)["prompt"]


st.title("Main Bot prompt")
prompt = st.text_area("", value=current_prompt, label_visibility="collapsed")
st.button(
    "Save",
    on_click=create_new_prompt,
    args=([prompt, bot_id]),
    disabled=prompt == current_prompt,
)
