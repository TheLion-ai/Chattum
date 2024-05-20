"""Api for communication with the bot with the frontend."""

import streamlit as st
import streamlit.components.v1 as components
from components.sidebar import sidebar_controller
from constants import EXTERNAL_BACKEND_URL, USERNAME
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected

st.set_page_config(
    page_title="API | Chattum",
    page_icon="🔄",
)

# default = None, TODO change to empty string, currently it is not working
bot_id = query_params.get_from_url_or_state("bot_id") or "None"
workflow_id = query_params.get_from_url_or_state("workflow_id") or "None"

ensure_bot_or_workflow_selected()
sidebar_controller()
query_params = ""
if bot_id:
    query_params += f"?bot_id={bot_id}"
if workflow_id:
    query_params += (
        f"&workflow_id={workflow_id}" if query_params else f"?workflow_id={workflow_id}"
    )

components.iframe(
    f"{EXTERNAL_BACKEND_URL}/docs/{USERNAME}{query_params}",
    height=1200,
    scrolling=True,
)
