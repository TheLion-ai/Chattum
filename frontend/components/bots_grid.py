"""This module contains the Bots Grid class which is used to display and select from available bots or create a new one."""

import streamlit as st
from backend_controller import create_new_bot, get_bots
from utils import query_params


class BotsGrid:
    """Used to display bots and manage them."""

    def __init__(self) -> None:
        """Initialize the current bot state."""
        # st.session_state.current_bot = query_params.get_form_url("bot_id")

    def __call__(self) -> None:
        """Create a view with available bots and a card for creating new bots."""
        self._display_new_bot_card()
        search_bar = st.text_input("Search")
        self._display_bots(search_bar)

    def _select_bot(self, bot_id: str) -> None:
        st.session_state.bot_id = bot_id
        st.session_state.sidebar_state = "Expanded"
        st.query_params["bot_id"] = bot_id

    def _display_new_bot_card(self) -> None:
        col1, _, _ = st.columns(3)
        with col1:
            with st.expander("Create a new bot", expanded=False):
                bot_name = st.text_input(
                    "Bot name"
                )  # TODO validator to ensure the name is not en empty string
                st.button("Create", on_click=create_new_bot, args=([bot_name]))
        st.write("")

    def _display_bots(self, search: str) -> None:
        bots = get_bots()
        if search:
            bots = [bot for bot in bots if search in bot["name"]]
        col1, col2, col3 = st.columns(3)

        for idx, bot in enumerate(bots):
            col_idx = idx % 3
            if col_idx == 0:
                col = col1
            elif col_idx == 1:
                col = col2
            else:
                col = col3
            with col:
                with st.form(key=f"bot-{idx}"):
                    # with st.expander(bot["name"], expanded=True):
                    st.markdown(f"### {bot['name']}")
                    if bot["prompt"] is not None and bot["prompt"] != "":
                        st.text(bot["prompt"][:300] + "...")
                    st.form_submit_button(
                        (
                            "Selected"
                            if query_params.get_form_url("bot_id") == bot["id"]
                            else "Select"
                        ),
                        type=(
                            "primary"
                            if query_params.get_form_url("bot_id") == bot["id"]
                            else "secondary"
                        ),
                        on_click=self._select_bot,
                        args=([bot["id"]]),
                    )
