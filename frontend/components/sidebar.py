"""This module contains the sidebar controller class which is used to control the sidebar stat."""

import streamlit as st
from constants import BOT_PAGES, WORKFLOW_PAGES
from st_pages import hide_pages, show_pages
from streamlit_extras.app_logo import add_logo

st.session_state.sidebar_state = "Hidden"


def show_bot_pages() -> None:
    hide_pages(WORKFLOW_PAGES)
    show_pages(BOT_PAGES)


def show_workflow_pages() -> None:
    hide_pages(BOT_PAGES)
    show_pages(WORKFLOW_PAGES)


def render_hidden_sidebar() -> None:
    """Render the hidden sidebar."""
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]{
            visibility: hidden;
        }
        """,
        unsafe_allow_html=True,
    )


def render_expanded_sidebar() -> None:
    """Render the expanded sidebar."""
    if st.query_params.get("bot_id"):
        show_bot_pages()
    elif st.query_params.get("workflow_id"):
        show_workflow_pages()

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]{
            visibility: visible;

        }
        [data-testid="stSidebarNav"] {
            background-image: url(https://i.ibb.co/8PswYTB/Chattum-600x600.png);
            background-repeat: no-repeat;
            background-position: 30px 10px;
            background-size: 220px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def expand_sidebar() -> None:
    """Change the sidebar state to expanded."""
    st.session_state.sidebar_state = "Expanded"


def hide_sidebar() -> None:
    """Change the sidebar state to hidden."""
    st.session_state.sidebar_state = "Hidden"


def sidebar_controller(state: str = None) -> None:
    """Show hidden or expanded sidebar depending on the state."""

    if "bot_id" not in st.query_params and "workflow_id" not in st.query_params:
        render_hidden_sidebar()
    else:
        render_expanded_sidebar()
