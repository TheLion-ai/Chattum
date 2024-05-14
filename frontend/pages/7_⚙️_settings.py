"""Settings page."""

import streamlit as st
from backend_controller import get_available_models, get_bot, get_model
from components.models import ModelPanel
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="Settings | Chattum",
    page_icon="⚙️",
)

bot_id = query_params.get_from_url_or_state("bot_id")
workflow_id = query_params.get_from_url_or_state("workflow_id")

ensure_bot_or_workflow_selected()
sidebar_controller()


st.title("Settings")
# st.write(get_bot(bot_id))

model_panel = ModelPanel(bot_id or workflow_id)
model_panel()
