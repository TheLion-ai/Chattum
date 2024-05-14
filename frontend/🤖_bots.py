"""Page for managing user bots."""

import streamlit as st
from components import bots_grid
from components.bot_menu import BotMenu
from components.sidebar import sidebar_controller
from utils import query_params, set_streamlit_page_config_once

set_streamlit_page_config_once()
current_bot = query_params.get_form_url("bot_id")


# pages = {
#     "Settings": {
#         "icon": "gear",
#         "content": render_settings,
#     },
#     "Prompt": {
#         "icon": "bi-terminal",
#         "content": render_prompt,
#     },
#     "Tools": {
#         "icon": "tools",
#         "content": render_tools,
#     },
#     "Sources": {
#         "icon": "file-earmark",
#         "content": render_sources,
#     },
#     "Conversations": {
#         "icon": "chat-square-text",
#         "content": render_conversations,
#     },
#     "Chat": {
#         "icon": "chat",
#         "content": render_chat,
#     },
#     "API": {
#         "icon": "link-45deg",
#         "content": render_api,
#     },
# }
sidebar_controller()
bots_grid()

# navbar = BotMenu(pages)
# navbar(current_bot)

selected_page = st.session_state.get("page")
# selected_page = selected_page or list(pages.keys())[0]

# if current_bot is None:
# else:
#     pages[selected_page]["content"]()
