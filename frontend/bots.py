"""Page for managing user bots."""
import constants
import streamlit as st
from components import bots_grid
from components.sidebar import sidebar_controller

sidebar_controller()

st.title("Chattum")
bots_grid()
