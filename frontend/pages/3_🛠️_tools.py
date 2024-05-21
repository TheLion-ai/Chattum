"""Tools that the bot can use to perform actions."""

import streamlit as st
from components.authentication import protect_page
from components.sidebar import sidebar_controller
from components.tools import ToolsPanel
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="Tools | Chattum",
    page_icon="🛠️",
)

bot_id = query_params.get_from_url_or_state("bot_id")

ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()


st.title("Tools")
sidebar_controller()

# st.warning("Tools are currently in development.")

tools_panel = ToolsPanel(bot_id)
tools_panel()
