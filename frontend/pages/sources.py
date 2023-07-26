"""Sources of data for the bot."""
import streamlit as st
from components import SourcesGrid
from components.sidebar import sidebar_controller

st.session_state.current_bot = st.experimental_get_query_params()["bot_id"][0]
sidebar_controller(state="Expanded")

st.title("Sources")
sources_grid = SourcesGrid(st.session_state.current_bot)()
