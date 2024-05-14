"""This module contains the Bots Grid class which is used to display and select from available bots or create a new one."""

import streamlit as st
from streamlit_tags import st_tags
from backend_controller import create_new_bot, get_bots, create_new_workflow, get_workflows
from utils import query_params


class BotsGrid:
    """Used to display bots and manage them."""

    def __init__(self) -> None:
        """Initialize the current bot state."""
        # st.session_state.current_bot = query_params.get_form_url("bot_id")
        

    def __call__(self) -> None:
        """Create a view with available bots and a card for creating new bots."""
        self._display_new_bot_or_workflow_card()
        search_bar = st.text_input("Search")
        self._create_workflow_from_state()
        self._display_bots_and_workflows(search_bar)

    def _select_bot(self, bot_id: str) -> None:
        st.session_state.bot_id = bot_id
        if "workflow_id" in st.session_state:
            del st.session_state.workflow_id
        st.session_state.sidebar_state = "Expanded"
        st.query_params["bot_id"] = bot_id
        if "workflow_id" in st.query_params:
            del st.query_params.workflow_id

    def _select_workflow(self, workflow_id: str) -> None:
        st.session_state.workflow_id = workflow_id
        if "bot_id" in st.session_state:
            del  st.session_state.bot_id
        st.session_state.sidebar_state = "Expanded"
        st.query_params["workflow_id"] = workflow_id
        if "bot_id" in st.query_params:
            del st.query_params.bot_id

    def _create_workflow_from_state(self) -> None:
        # check if there are aready set parameters for workflow creation
        if 'workflow_params' in st.session_state:
            params = st.session_state.workflow_params
            create_new_workflow(params['workflow_name'],
                                params['workflow_task'],
                                params['workflow_classes'])
            del st.session_state['workflow_params']

    def process_workflow_creation(self, workflow_name: str) -> None:
        self._workflow_dialog(workflow_name)
        
    @st.experimental_dialog("Create new workflow task")
    def _workflow_dialog(self, workflow_name: str) -> None:
        workflow_task = st.selectbox("Select task", (
                    "Classification",
                    "Extraction",
                    "Generation"))
        if 'classification_classes' not in st.session_state:
            st.session_state.classification_classes = []
        if workflow_task == "Classification":
            keywords = st_tags(
                            label='# Enter classes names:',
                            text='Press enter to add more',
                            value=['Class 1', 'Class 2'],
                            suggestions=['cat', 'dog', 'parrot', 'fish'],
                            maxtags = 10,
                            key='classification_keywords')
        else:
            keywords = []

        # the following only creates the workflow params in session state
        # due to the: https://github.com/streamlit/streamlit/issues/3223
        # the toast with response casues "Bad message format: setIn cannot 
        # be called on an ElementNode" if the dialog is opened
        if st.button("Create workflow"):
            self.create_new_workflow_params(workflow_name, workflow_task, keywords)
            st.rerun()

    def create_new_workflow_params(self, workflow_name: str, workflow_task: str, keywords: list[str]) -> None:
        st.session_state.workflow_params = {
            "workflow_name": workflow_name,
            "workflow_task": workflow_task,
            "workflow_classes": keywords
        }

    def _save_classes(self, classes: list[str]) -> None:
        st.session_state.classification_classes = classes

    def _display_new_bot_or_workflow_card(self) -> None:
        col1, col2, _ = st.columns(3)
        with col1:
            with st.expander("Create a new bot", expanded=False):
                bot_name = st.text_input(
                    "Bot name"
                )  # TODO validator to ensure the name is not en empty string
                st.button("Create", on_click=create_new_bot, args=([bot_name]), key="create_bot")
        with col2:
            with st.expander("Create a new workflow", expanded=False):
                workflow_name = st.text_input(
                    "Workflow name"
                )
                    
                create_classes = st.button("Create workflow",
                          key="create_workflow")
                if create_classes:
                    self.process_workflow_creation(workflow_name)
        st.write("")


    def _display_bots_and_workflows(self, search: str) -> None:
        bots = get_bots()
        for bot in bots:
            bot['type'] = 'bot'
        workflows = get_workflows()
        for workflow in workflows:
            workflow['type'] = 'workflow'

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
                with st.form(key=f"item-{idx}"):
                    col_name, col_type = st.columns([6, 1])
                    with col_name:
                        st.markdown(f"### {item['name']}")
                    with col_type:
                        st.markdown(f"<small><i>{item['type']}</i></small>", unsafe_allow_html=True)
            
                    if "prompt" in item and item["prompt"] is not None and item["prompt"] != "":
                        st.text(item["prompt"][:300] + "...")
                    
                    click_func = self._select_bot if item["type"] == "bot" else self._select_workflow
                    st.form_submit_button(
                        (
                            "Selected"
                            if query_params.get_form_url("bot_id") == item["id"]
                            else "Select"
                        ),
                        type=(
                            "primary"
                            if query_params.get_form_url("bot_id") == item["id"]
                            else "secondary"
                        ),
                        on_click=click_func,
                        args=([item["id"]]),
                    )
