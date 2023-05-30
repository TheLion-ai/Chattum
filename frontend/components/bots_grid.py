"""This module contains the Bots Grid class which is used to display and select from available bots or create a new one."""

import streamlit as st
from backend_controller import create_new_bot, get_bots

from .sidebar import expand_sidebar


class BotsGrid:
    """Used to display bots and manage them."""

    def __init__(self) -> None:
        """Initialize the current bot state."""
        if "bot_id" in st.experimental_get_query_params():
            st.session_state.current_bot = st.experimental_get_query_params()["bot_id"][
                0
            ]

    def __call__(self) -> None:
        """Create a view with available bots and a card for creating new bots."""
        self._display_new_bot_card()
        self._display_bots()

    def _select_bot(self, bot_id: str) -> None:
        st.session_state.current_bot = bot_id
        st.experimental_set_query_params(bot_id=bot_id)
        expand_sidebar()

    def _display_new_bot_card(self) -> None:
        col1, _, _ = st.columns(3)
        with col1:
            with st.expander("Create a new bot", expanded=True):
                bot_name = st.text_input(
                    "Bot name"
                )  # TODO validator to ensure the name is not en empty string
                st.button("'Create'", on_click=create_new_bot, args=([bot_name]))
        st.write("")

    def _display_bots(self) -> None:
        bots = get_bots()
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
                with st.expander(bot["name"], expanded=True):
                    st.button(
                        "Selected"
                        if st.session_state.get("current_bot", None) == bot["id"]
                        else "Select",
                        key=idx,
                        type="primary"
                        if st.session_state.get("current_bot", None) == bot["id"]
                        else "secondary",
                        on_click=self._select_bot,
                        args=([bot["id"]]),
                    )
