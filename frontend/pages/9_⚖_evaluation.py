"""Settings page."""

import streamlit as st
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="Settings | Chattum",
    page_icon="⚖",
)

bot_id = query_params.get_from_url_or_state("workflow_id")

ensure_bot_or_workflow_selected()
sidebar_controller()


st.title("Evaluation")
# st.write(get_bot(workflow_id))
