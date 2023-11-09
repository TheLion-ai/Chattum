"""File for storing constants used in the frontend app."""
import streamlit as st

BACKEND_URL = "http://backend:5000"
EXTERNAL_BACKEND_URL = "http://localhost:8000"
USERNAME = "chattum"

st.session_state.username = "chattum"
st.session_state.current_bot = st.session_state.get("current_bot", None)