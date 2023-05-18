"""Page for managing user bots."""
import streamlit as st
from components import BotsGrid, sidebar_controller

# construct UI layout
st.title("Chattum")
bots_grid = BotsGrid()
bots_grid()
