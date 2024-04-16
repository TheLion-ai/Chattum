"""File for storing constants used in the frontend app."""

import os

import streamlit as st

BACKEND_URL = os.environ.get("BACKEND_URL") or "http://backend:5000"
EXTERNAL_BACKEND_URL = os.environ.get("EXTERNAL_BACKEND_URL") or "http://localhost:8000"
USERNAME = "chattum"

st.session_state.username = "chattum"
st.session_state.current_bot = st.session_state.get("current_bot", None)
