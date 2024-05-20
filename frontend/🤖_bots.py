"""Page for managing user bots."""

import streamlit as st
from components import bots_grid
from components.bot_menu import BotMenu
from components.sidebar import sidebar_controller
from utils import query_params, set_streamlit_page_config_once

set_streamlit_page_config_once()
current_bot = query_params.get_form_url("bot_id")


sidebar_controller()
bots_grid()


selected_page = st.session_state.get("page")
