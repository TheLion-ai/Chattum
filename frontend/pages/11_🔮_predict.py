import streamlit as st
from backend_controller import (
    change_instructions,
    get_model,
    get_workflow,
    run_prediction,
)
from components.authentication import protect_page
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="Predict | Chattum",
    page_icon="🔮",
)

workflow_id = query_params.get_from_url_or_state("workflow_id")


ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()

input_container = st.container()
debug_container = st.container()


with input_container:
    # with st.form(key="chat_input", clear_on_submit=True):
    # user_input = st.text_area("Type your message:", key="input", height=100)
    # submit_button = st.form_submit_button(label="Send")
    message = st.chat_input("Type your message:", key="input")

    if message:
        input_container.empty()
        with st.spinner("Thinking..."):
            response = run_prediction(workflow_id, message)
            if response is not None:
                out_message = (response,)
                st.json(out_message)
