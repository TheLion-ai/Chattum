"""File for storing constants used in the frontend app."""

import os

import streamlit as st
from st_pages import Page

BACKEND_URL = os.environ.get("BACKEND_URL") or "http://backend:5000"
EXTERNAL_BACKEND_URL = os.environ.get("EXTERNAL_BACKEND_URL") or "http://localhost:8000"
USERNAME = "chattum"

BOT_PAGES = [
    Page("🤖_bots.py", "Bots", "🤖"),
    Page("pages/1_📝_prompt.py", "Prompt", "📝"),
    Page("pages/2_📑_sources.py", "Sources", "📑"),
    Page("pages/3_🛠️_tools.py", "Tools", "🛠️"),
    Page("pages/4_🗣️_chat.py", "Chat", "🗣️"),
    Page("pages/5_💬_conversations.py", "Conversations", "💬"),
    Page("pages/6_🔄_API.py", "API", "🔄"),
    Page("pages/7_⚙️_settings.py", "Settings", "⚙️"),
]
WORKFLOW_PAGES = [

    Page('pages/6_🔄_API.py', "API", "🔄"),
    Page('pages/7_⚙️_settings.py', "Settings", "⚙️"),
    Page('pages/8_🔬_calibration.py', "Calibration", "🔬"),
    Page('pages/9_⚖_evaluation.py', "Evaluation", "⚖"),
    Page('pages/10_📝_instructions.py', "Instructions", "📝"),
    Page('pages/11_🔮_predict.py', "Predict", "🔮"),
 ]


st.session_state.username = "chattum"
st.session_state.current_bot = st.session_state.get("current_bot", None)
