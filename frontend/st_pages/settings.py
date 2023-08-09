"""Settings page."""

import streamlit as st
from backend_controller import get_bot
from components.sidebar import sidebar_controller
from utils import query_params


def render_settings() -> None:
    """Render the settings page."""
    bot_id = query_params.get_form_url("bot_id")

    st.title("Settings")
    st.write(get_bot(bot_id))
