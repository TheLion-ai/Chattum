"""Api for communication with the bot with the frontend."""
import streamlit.components.v1 as components
from constants import BACKEND_URL

components.iframe(f"{BACKEND_URL}/docs", height=800, scrolling=True)
