"""This module contains the SourcesGrid class which is used to display and select from available sources or create a new one."""

from io import BytesIO

import streamlit as st
import streamlit.components.v1 as components
from backend_controller import (
    create_new_source,
    delete_source,
    get_source_file,
    get_sources,
)
from components.delete_modal import DeleteModal
from streamlit_modal import Modal


class SourcesGrid:
    """Used to display sources and manage them."""

    def __init__(self, bot_id: str) -> None:
        """Initialize the current bot state.

        Args:
            bot_id (str): id of the current bot
        """
        self.bot_id = bot_id

        self.delete_modal = DeleteModal(
            "Delete source", key="delete_source_modal", delete_function=delete_source
        )
        self.sources = get_sources(self.bot_id)["sources"]
        if "disabled" not in st.session_state:
            st.session_state.disabled = False

    def __call__(self) -> None:
        """Create a view with available sources and a card for creating new sources."""
        self.delete_modal()

        self._display_new_source_card()
        self._display_sources()

    def _display_new_source_card(self) -> None:
        """Display a card for creating new sources."""
        with st.container():
            with st.expander("Add new source", expanded=False):
                source_type = st.selectbox("File", ["url", "pdf", "xls", "txt"])
                with st.form(clear_on_submit=True, key="File submit"):
                    source_name = st.text_input(
                        "Name",
                    )
                    if source_type == "url":
                        url = st.text_input("URL")
                        source_file = None
                    elif source_type == "txt":
                        text = st.text_area("Text", key="text")
                    else:
                        source_file = st.file_uploader("File")
                        url = None

                    st.session_state.disabled = source_name != ""

                    submit = st.form_submit_button("Add", type="secondary")
                    if submit:
                        if source_name.replace(" ", "") == "" or (
                            source_type == "url" and url.replace(" ", "") == ""
                        ):
                            st.warning("Please fill in all fields")
                        else:
                            if source_type == "url":
                                create_new_source(
                                    source_name,
                                    source_type,
                                    self.bot_id,
                                    file=None,
                                    url=url,
                                )
                            else:
                                if source_type == "txt":
                                    file = BytesIO(text.encode("utf-8"))
                                else:
                                    file = source_file.getvalue()  # type: ignore
                                create_new_source(
                                    source_name,
                                    source_type,
                                    self.bot_id,
                                    file=file,  # type: ignore
                                    url=None,
                                )
                        self.sources = get_sources(self.bot_id)["sources"]

        st.write("")

    def _display_sources(self) -> None:
        """Display available sources."""
        if len(self.sources) > 0:
            for source in self.sources:
                with st.expander(source["name"], expanded=False):
                    delete_button = st.button(
                        "Delete",
                        args=([source["id"]]),
                        key=f"delete_source_{source['id']}",
                    )

                    if delete_button:
                        delete_source(self.bot_id, source["id"])

                        st.experimental_rerun()
                    st.write(f"ID: {source['id']}")
                    st.write(f"Type: {source['source_type']}")

                    file_extension = source["source_type"]
                    if source["source_type"] == "txt" or source["source_type"] == "url":
                        text = get_source_file(self.bot_id, source["id"]).decode(
                            "utf-8"
                        )
                        new_text = st.text_area(
                            "Text", text, key=f"text_{source['id']}"
                        )
                        if new_text != text:
                            update_button = st.button(
                                "Update", key=f"update_{source['id']}"
                            )
                            if update_button:
                                file = BytesIO(new_text.encode("utf-8"))
                                create_new_source(
                                    source["name"],
                                    source["source_type"],
                                    self.bot_id,
                                    file=file,
                                    source_id=source["id"],
                                )
                    else:
                        st.download_button(
                            "Download file",
                            data=get_source_file(self.bot_id, source["id"]),
                            file_name=f"{source['name']}.{file_extension}",
                            mime=None,
                            key=f"download_pdf_{source['id']}",
                        )
