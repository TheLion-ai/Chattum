"""This module contains the SourcesGrid class which is used to display and select from available sources or create a new one."""

import streamlit as st
from backend_controller import (
    create_new_source,
    delete_source,
    get_source,
    get_source_file,
    get_sources,
)


class SourcesGrid:
    """Used to display sources and manage them."""

    def __init__(self, bot_id: str) -> None:
        """Initialize the current bot state.

        Args:
            bot_id (str): id of the current bot
        """
        self.bot_id = bot_id

    def __call__(self) -> None:
        """Create a view with available sources and a card for creating new sources."""
        self._display_new_source_card()
        self._display_sources()

    def _display_new_source_card(self) -> None:
        with st.container():
            with st.expander("Add new source", expanded=False):
                with st.form(clear_on_submit=True, key="File submit"):
                    source_name = st.text_input("Name")
                    source_type = st.selectbox("File", ["pdf", "url", "xls", "txt"])
                    if source_type == "url":
                        source_file = st.text_input("URL")
                    else:
                        source_file = st.file_uploader("File")
                    submit = st.form_submit_button("Add")
                    if submit:
                        create_new_source(
                            source_file, source_name, source_type, self.bot_id
                        )

        st.write("")

    def _display_sources(self) -> None:
        sources = get_sources(self.bot_id)["sources"]
        if len(sources) > 0:
            for idx, source_id in enumerate(sources):
                source = get_source(self.bot_id, source_id)

                with st.container():
                    with st.expander(source["name"], expanded=False):
                        st.button(
                            "Delete",
                            on_click=delete_source,
                            args=([self.bot_id, source_id]),
                            key=f"delete_source_{idx}",
                        )
                        st.write(f"ID: {source['id']}")
                        st.write(f"Type: {source['source_type']}")
                        if source["source_type"] == "url":
                            st.write(f"URL: {source['file']}")
                        elif source["source_type"] == "pdf":
                            st.download_button(
                                "Download file",
                                data=get_source_file(self.bot_id, source_id),
                                file_name=f"{source['name']}.{source['source_type']}",
                                mime=None,
                                key=f"download_pdf_{idx}",
                            )  # "application/octet-stream")
                        elif source["source_type"] == "xls":
                            st.download_button(
                                "Download file",
                                data=get_source_file(self.bot_id, source_id),
                                file_name=f"{source['name']}.{source['source_type']}",
                                mime="text/xls",
                                key=f"download_xls_{idx}",
                            )
                        elif source["source_type"] == "txt":
                            st.download_button(
                                "Download file",
                                data=get_source_file(self.bot_id, source_id),
                                file_name=f"{source['name']}.{source['source_type']}",
                                mime="text/plain",
                                key=f"download_txt_{idx}",
                            )
