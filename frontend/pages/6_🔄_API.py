"""Api for communication with the bot with the frontend."""

import streamlit.components.v1 as components
from components.sidebar import sidebar_controller
from constants import EXTERNAL_BACKEND_URL, USERNAME
from utils import query_params
from utils.page_config import ensure_bot_selected

bot_id = query_params.get_from_url_or_state("bot_id")

ensure_bot_selected()
sidebar_controller()

components.iframe(
    f"{EXTERNAL_BACKEND_URL}/docs/{USERNAME}/{bot_id}",
    height=1200,
    scrolling=True,
)
