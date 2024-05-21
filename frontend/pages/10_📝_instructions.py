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
from components.authentication import protect_page
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
protect_page()


st.title("Settings")
# st.write(get_bot(workflow_id))

workflow = get_workflow(workflow_id)
st.session_state["new_workflow"] = copy.deepcopy(workflow)
# st.write(workflow)
if workflow["task"].lower() == "classification":

    st.session_state["new_workflow"]["classes"] = st_tags(
        label="#### Classes",
        text="Press enter to add more",
        value=workflow.get("classes", []),
        suggestions=["cat", "dog", "parrot", "fish"],
        maxtags=10,
        key="classification_keywords",
    )
    st.write("#### Additional instructions:")
    st.session_state["new_workflow"]["instructions"] = st_ace(
        value=workflow.get("instructions", ""), language="markdown", auto_update=True
    )
    if st.session_state["new_workflow"]["classes"] == workflow["classes"]:
        st.write("#### Class thresholds:")
        class_thresholds = workflow.get("class_thresholds") if workflow else None
        if class_thresholds is not None:
            for class_name, threshold in class_thresholds.items():
                st.session_state["new_workflow"]["class_thresholds"][
                    class_name
                ] = st.number_input(value=threshold, label=class_name, key=class_name)
elif workflow["task"].lower() == "extraction":
    with st.container(border=True):
        with st.container(border=True):
            for i in range(len(st.session_state.new_workflow["entities"])):
                col1, col2, col3 = st.columns([3, 3, 1])
                with col1:
                    st.session_state.new_workflow["entities"][i][0] = st.text_input(
                        "Entity name",
                        key=f"entity_name_{i}",
                        label_visibility="collapsed",
                        placeholder="Entity name",
                        value=st.session_state.new_workflow["entities"][i][0],
                    )
                with col2:
                    st.session_state.new_workflow["entities"][i][1] = st.text_input(
                        "Entity type",
                        key=f"entity_type_{i}",
                        label_visibility="collapsed",
                        placeholder="Type e.g. date, location, etc.",
                        value=st.session_state.new_workflow["entities"][i][1],
                    )
                with col3:
                    if st.button("Remove", use_container_width=True, key=f"remove_{i}"):
                        del st.session_state.new_workflow["entities"][i]
                        st.rerun()
            _, col2, _ = st.columns([2, 3, 2])
            with col2:
                if st.button("Add entity", key="add_entity", use_container_width=True):
                    st.session_state.new_workflow["entities"].append(["", ""])
                    st.rerun()
    st.session_state.new_workflow["instructions"] = st.text_area(
        "Additional instructions (optional)"
    )


if st.button("Save"):
    create_or_edit_workflow(st.session_state["new_workflow"])
    st.experimental_rerun()
    # change_instructions(workflow_id, instructions, keywords)
