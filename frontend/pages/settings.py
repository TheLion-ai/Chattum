"""Settings page."""

import streamlit as st

from frontend.components.sidebar_controller import sidebar_controller

sidebar_controller("Hidden")

st.title("Settings")
