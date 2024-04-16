"""Settings page."""

import streamlit as st
from backend_controller import get_available_models, get_bot, get_model
from components.models import ModelPanel
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_selected

bot_id = query_params.get_from_url_or_state("bot_id")

ensure_bot_selected()
sidebar_controller()


st.title("Settings")
# st.write(get_bot(bot_id))

model_panel = ModelPanel(bot_id)
model_panel()
