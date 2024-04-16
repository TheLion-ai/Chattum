"""Tools that the bot can use to perform actions."""

import streamlit as st
from components.sidebar import sidebar_controller
from components.tools import ToolsPanel
from utils import query_params
from utils.page_config import ensure_bot_selected

bot_id = query_params.get_from_url_or_state("bot_id")

ensure_bot_selected()
sidebar_controller()


st.title("Tools")
sidebar_controller()

# st.warning("Tools are currently in development.")

tools_panel = ToolsPanel(bot_id)
tools_panel()
