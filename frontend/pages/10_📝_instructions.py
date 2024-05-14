"""Settings page."""

import streamlit as st
from backend_controller import get_available_models, get_model, get_workflow, change_instructions
from components.models import ModelPanel
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
from streamlit_tags import st_tags
from streamlit_ace import st_ace

st.set_page_config(
    page_title="Settings | Chattum",
    page_icon="⚙️",
)

workflow_id = query_params.get_from_url_or_state("workflow_id")


ensure_bot_or_workflow_selected()
sidebar_controller()


st.title("Instructions")
# st.write(get_bot(workflow_id))

workflow = get_workflow(workflow_id)
# st.write(workflow)

keywords = st_tags(
    label='#### Enter classes names:',
    text='Press enter to add more',
    value=workflow.get('classes', []),
    suggestions=['cat', 'dog', 'parrot', 'fish'],
    maxtags = 10,
    key='classification_keywords')

instructions = st_ace(value=workflow.get('instructions', ''), language="markdown", auto_update=True)
if st.button("Save"):
    change_instructions(workflow_id, instructions, keywords)

