"""Api for communication with the bot with the frontend."""
import streamlit.components.v1 as components
from constants import EXTERNAL_BACKEND_URL, USERNAME
from utils import query_params


def render_api() -> None:
    """Render the api page."""
    current_bot = query_params.get_form_url("bot_id")
    components.iframe(
        f"{EXTERNAL_BACKEND_URL}/docs/{USERNAME}/{current_bot}",
        height=1200,
        scrolling=True,
    )
