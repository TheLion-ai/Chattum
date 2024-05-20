"""This module contains the Bots Grid class which is used to display and select from available bots or create a new one."""

import streamlit as st
from backend_controller import (
    create_new_bot,
    create_new_workflow,
    get_bots,
    get_workflows,
)
from streamlit_extras.colored_header import colored_header
from streamlit_tags import st_tags
from utils import query_params


class BotsGrid:
    """Used to display bots and manage them."""

    def __init__(self) -> None:
        """Initialize the current bot state."""
        # st.session_state.current_bot = query_params.get_form_url("bot_id")

    def __call__(self) -> None:
        """Create a view with available bots and a card for creating new bots."""
        if (
            st.session_state.get("creating_workflow", False) is False
            and st.session_state.get("creating_bot", False) is False
        ):
            self._display_new_bot_or_workflow_card()
        elif st.session_state.get("creating_workflow", False):
            self.process_workflow_creation()
        elif st.session_state.get("creating_bot", False):
            self.process_bot_creation()
        search_bar = st.text_input("Search", on_change=self._display_bots_and_workflows)
        self._display_bots_and_workflows(search_bar)

    def _select_bot(self, bot_id: str) -> None:
        st.session_state.bot_id = bot_id
        if "workflow_id" in st.session_state:
            del st.session_state.workflow_id
        st.session_state.sidebar_state = "Expanded"
        query_params.set_to_url_and_state(bot_id=bot_id)
        if "workflow_id" in st.query_params:
            del st.query_params.workflow_id

    def _select_workflow(self, workflow_id: str) -> None:
        st.session_state.workflow_id = workflow_id
        if "bot_id" in st.session_state:
            del st.session_state.bot_id
        st.session_state.sidebar_state = "Expanded"
        query_params.set_to_url_and_state(workflow_id=workflow_id)
        if "bot_id" in st.query_params:
            del st.query_params.bot_id

    def process_bot_creation(self) -> None:
        with st.container(border=True):
            bot_name = st.text_input(
                "Bot name"
            )  # TODO validator to ensure the name is not en empty string

            col1, _, col2 = st.columns([1, 3, 1])
            with col1:
                if st.button("Create bot"):
                    create_new_bot(bot_name)
                    st.session_state.creating_bot = False
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.creating_bot = False
                    st.rerun()

    def process_workflow_creation(self) -> None:
        with st.container(border=True):
            if "new_workflow" not in st.session_state:
                st.session_state.new_workflow = {
                    "name": "",
                    "task": "",
                    "entities": [],
                    "classes": None,
                    "instructions": None,
                }
            st.session_state.new_workflow["name"] = st.text_input(
                "Workflow name", value=st.session_state.new_workflow.get("name", "")
            )
            st.session_state.new_workflow["task"] = st.selectbox(
                "Select task",
                ("Classification", "Extraction"),
                index=(
                    0
                    if st.session_state.new_workflow.get("task", "") == "Classification"
                    else 1
                ),
            )

            if st.session_state.new_workflow["task"] == "Classification":
                st.session_state.new_workflow["classes"] = st_tags(
                    label="Enter classes names:",
                    text="Press enter to add more",
                    suggestions=["cat", "dog", "parrot", "fish"],
                    maxtags=10,
                    value=st.session_state.new_workflow.get("classes", []),
                    key="classification_keywords",
                )
            else:
                with st.container(border=True):
                    for i in range(len(st.session_state.new_workflow["entities"])):
                        col1, col2, col3 = st.columns([3, 3, 1])
                        with col1:
                            st.session_state.new_workflow["entities"][i][
                                0
                            ] = st.text_input(
                                "Entity name",
                                key=f"entity_name_{i}",
                                label_visibility="collapsed",
                                placeholder="Entity name",
                                value=st.session_state.new_workflow["entities"][i][0],
                            )
                        with col2:
                            st.session_state.new_workflow["entities"][i][
                                1
                            ] = st.text_input(
                                "Entity type",
                                key=f"entity_type_{i}",
                                label_visibility="collapsed",
                                placeholder="Type e.g. date, location, etc.",
                                value=st.session_state.new_workflow["entities"][i][1],
                            )
                        with col3:
                            if st.button(
                                "Remove", use_container_width=True, key=f"remove_{i}"
                            ):
                                del st.session_state.new_workflow["entities"][i]
                                st.rerun()
                    _, col2, _ = st.columns([2, 3, 2])
                    with col2:
                        if st.button(
                            "Add entity", key="add_entity", use_container_width=True
                        ):
                            st.session_state.new_workflow["entities"].append(["", ""])
                            st.rerun()
            st.session_state.new_workflow["instructions"] = st.text_area(
                "Additional instructions (optional)"
            )

            col1, _, col2 = st.columns([1, 3, 1])
            with col1:
                if st.button("Create workflow"):
                    create_new_workflow(st.session_state.new_workflow)
                    del st.session_state.new_workflow
                    st.session_state.creating_workflow = False
                    st.rerun()
            with col2:
                if st.button("Cancel", use_container_width=True):
                    del st.session_state.new_workflow
                    st.session_state.creating_workflow = False
                    st.rerun()

    def _display_new_bot_or_workflow_card(self) -> None:
        col1, col2, _ = st.columns(3)
        with col1:
            st.button(
                "Create a new bot",
                on_click=lambda: query_params.set_to_url_and_state(creating_bot=True),
                use_container_width=True,
            )

        with col2:
            st.button(
                "Create a new workflow",
                on_click=lambda: query_params.set_to_url_and_state(
                    creating_workflow=True
                ),
                use_container_width=True,
            )
        st.write("")

    def _display_bots_and_workflows(self, search: str) -> None:
        bots = get_bots()
        for bot in bots:
            bot["type"] = "bot"
        workflows = get_workflows()
        for workflow in workflows:
            workflow["type"] = "workflow"

        items = bots + workflows

        if search:
            items = [item for item in items if search in item["name"]]
        col1, col2, col3 = st.columns(3)

        for idx, item in enumerate(items):
            col_idx = idx % 3
            if col_idx == 0:
                col = col1
            elif col_idx == 1:
                col = col2
            else:
                col = col3
            with col:
                with st.container(border=True, height=220):
                    # col_name, col_type = st.columns([6, 1])
                    # with col_name:
                    #     st.markdown(f"### {item['name']}")
                    # with col_type:
                    #     st.markdown(f"<small><i>{item['type']}</i></small>", unsafe_allow_html=True)
                    color_name = "blue-70" if item["type"] == "bot" else "green-70"
                    colored_header(
                        label=item["name"],
                        color_name=color_name,
                        description=item["type"],
                    )

                    if (
                        "prompt" in item
                        and item["prompt"] is not None
                        and item["prompt"] != ""
                    ):
                        st.text(item["prompt"].split("\n")[0][:50] + "...")
                    else:
                        st.text("...")

                    click_func = (
                        self._select_bot
                        if item["type"] == "bot"
                        else self._select_workflow
                    )
                    st.button(
                        (
                            "Selected"
                            if item["id"]
                            in [
                                query_params.get_from_url_or_state("bot_id"),
                                query_params.get_from_url_or_state("workflow_id"),
                            ]
                            else "Select"
                        ),
                        type=(
                            "primary"
                            if item["id"]
                            in [
                                query_params.get_from_url_or_state("bot_id"),
                                query_params.get_from_url_or_state("workflow_id"),
                            ]
                            else "secondary"
                        ),
                        on_click=click_func,
                        args=([item["id"]]),
                        key=f"select_{item['id']}",
                    )
