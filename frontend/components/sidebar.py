"""This module contains the sidebar controller class which is used to control the sidebar stat."""

import streamlit as st

st.session_state.sidebar_state = "Hidden"


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
    st.markdown(
        """
        <style>
        [data-testid="stSidebar"]{
            visibility: visible;
        }
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
    if state is None:
        state = st.session_state.get("sidebar_state", "Hidden")

    if state == "Expanded":
        render_expanded_sidebar()

    elif state == "Hidden":
        render_hidden_sidebar()
    else:
        raise Exception(
            f"State {state} recognized should be one of the following : [Exapnded, Hidden]"
        )
