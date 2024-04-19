"""Sources of data for the bot."""

import streamlit as st
from components import SourcesGrid
from components.sidebar import sidebar_controller
from utils import query_params

st.set_page_config(
    page_title="Sources | Chattum",
    page_icon="📑",
)

bot_id = query_params.get_from_url_or_state("bot_id")

sidebar_controller()

st.title("Sources")
SourcesGrid(bot_id)()
