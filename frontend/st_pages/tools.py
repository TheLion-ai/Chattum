"""Tools that the bot can use to perform actions."""
import streamlit as st

from utils import query_params
from components.tools import ToolsPanel

def render_tools() -> None:
    """Render the tools page."""
    st.title("Tools")
    bot_id = query_params.get_form_url("bot_id")
    tools_panel = ToolsPanel(bot_id)
    tools_panel()
