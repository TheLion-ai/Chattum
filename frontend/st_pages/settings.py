"""Settings page."""

import streamlit as st
from backend_controller import get_available_models, get_bot, get_model
from components.models import ModelPanel
from components.sidebar import sidebar_controller
from utils import query_params


def render_settings() -> None:
    """Render the settings page."""
    bot_id = query_params.get_form_url("bot_id")

    st.title("Settings")
    # st.write(get_bot(bot_id))

    model_panel = ModelPanel(bot_id)
    model_panel()
