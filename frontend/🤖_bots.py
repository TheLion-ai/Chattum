"""Page for managing user bots."""

import streamlit as st
from components import bots_grid
from components.authentication import protect_page
from components.bot_menu import BotMenu
from components.sidebar import sidebar_controller
from utils import query_params, set_streamlit_page_config_once

set_streamlit_page_config_once()
sidebar_controller()
st.info(
    """\n
    This is a shared demo for all judges. Login 'demo' and password is 'demo' \n
    If the login screen doesn't appear refresh the streamlit app. \n
    Ass this demo is not secure so we advise against using your own api keys" \n
    Please see exmaple bots to copy our API keys that are created just for this demo and have usage limits
    """
)


protect_page()


bots_grid()


selected_page = st.session_state.get("page")
