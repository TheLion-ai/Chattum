"""Api for communication with the bot with the frontend."""
import streamlit.components.v1 as components
from constants import EXTERNAL_BACKEND_URL

components.iframe(f"{EXTERNAL_BACKEND_URL}/docs", height=800, scrolling=True)
