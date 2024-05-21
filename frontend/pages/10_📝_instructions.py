"""Settings page."""

import copy

import streamlit as st
from backend_controller import (
    change_instructions,
    create_or_edit_workflow,
    get_available_models,
    get_model,
    get_workflow,
)
from components.models import ModelPanel
from components.sidebar import sidebar_controller
from streamlit_ace import st_ace
from streamlit_tags import st_tags
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

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
edited_workflow = copy.deepcopy(workflow)
# st.write(workflow)

edited_workflow["classes"] = st_tags(
    label="#### Classes",
    text="Press enter to add more",
    value=workflow.get("classes", []),
    suggestions=["cat", "dog", "parrot", "fish"],
    maxtags=10,
    key="classification_keywords",
)
st.write("#### Additional instructions:")
edited_workflow["instructions"] = st_ace(
    value=workflow.get("instructions", ""), language="markdown", auto_update=True
)
if edited_workflow["classes"] == workflow["classes"]:
    st.write("#### Class thresholds:")
    class_thresholds = workflow.get("class_thresholds") if workflow else None
    if class_thresholds is not None:
        for class_name, threshold in class_thresholds.items():
            edited_workflow["class_thresholds"][class_name] = st.number_input(
                value=threshold, label=class_name, key=class_name
            )

if st.button("Save"):
    create_or_edit_workflow(edited_workflow)
    st.experimental_rerun()
    # change_instructions(workflow_id, instructions, keywords)
