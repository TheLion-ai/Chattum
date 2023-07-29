"""Page for managing user bots."""
import streamlit as st
from components import bots_grid
from components.bot_menu import BotMenu
from components.sidebar import sidebar_controller
from st_pages.chat import render_chat
from st_pages.conversations import render_conversations
from st_pages.prompt import render_prompt
from st_pages.settings import render_settings
from st_pages.sources import render_sources
from st_pages.tools import render_tools
from utils import query_params, set_streamlit_page_config_once

set_streamlit_page_config_once()
current_bot = query_params.get_form_url("bot_id")

pages = {
    "Settings": {
        "icon": "gear",
        "content": render_settings,
    },
    "Prompt": {
        "icon": "bi-terminal",
        "content": render_prompt,
    },
    "Tools": {
        "icon": "tools",
        "content": render_tools,
    },
    "Sources": {
        "icon": "file-earmark",
        "content": render_sources,
    },
    "Conversations": {
        "icon": "chat-square-text",
        "content": render_conversations,
    },
    "Chat": {
        "icon": "chat",
        "content": render_chat,
    },
}
sidebar_controller("Expanded")
navbar = BotMenu(pages)
navbar(current_bot)

selected_page = st.session_state.get("page")
selected_page = selected_page or list(pages.keys())[0]

if current_bot is None:
    bots_grid()
else:
    pages[selected_page]["content"]()
