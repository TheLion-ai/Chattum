"""This module contains DeleteModal class which is used to display a modal for deleting a source."""

from typing import Callable

import streamlit as st
from backend_controller import delete_source
from streamlit_modal import Modal


class DeleteModal:
    """Used to display a modal for deleting a source."""

    def __init__(self, title: str, key: str, delete_function: Callable) -> None:
        """Initialize the modal.

        Args:
            title (str): title of the modal
            key (str): key of the modal
            delete_function (Callable): function to call when the modal is confirmed
        """
        self.open_key = f"modal_{key}_open"
        self.args_key = f"modal_{key}_args"
        if self.open_key not in st.session_state:
            st.session_state[self.open_key] = False

        self.modal = Modal(title, key=key)

        if not self.modal.is_open() and st.session_state[self.open_key]:
            self.modal.open()
        if self.modal.is_open() and not st.session_state[self.open_key]:
            self.modal.close()

        self.delete_function = delete_function
        self.args = None

    def __call__(self) -> None:
        """Create a view with available sources and a card for creating new sources."""
        if st.session_state[self.open_key]:
            with self.modal.container():

                st.write("Do you really want to delete this source?")
                c1, c2 = st.columns(2)
                with c1:
                    modal_yes_button = st.button("Yes")
                    if modal_yes_button:
                        delete_source(*st.session_state[self.args_key])
                        self.close()

                with c2:
                    modal_no_button = st.button("No")
                    if modal_no_button:
                        self.close()

        if not self.modal.is_open() and st.session_state[self.open_key]:
            st.session_state[self.open_key] = False

    def open(self, args: list = []) -> None:
        """Open the modal.

        Args:
            args (tuple): arguments to pass to the delete function
        """
        st.session_state[self.args_key] = args
        st.session_state[self.open_key] = True

    def close(self) -> None:
        """Close the modal."""
        st.session_state[self.open_key] = False
        self.modal.close()
