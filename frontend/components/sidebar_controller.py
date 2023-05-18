"""This module contains the sidebar controller class which is used to control the sidebar stat."""

import streamlit as st


class SideBarController:
    """Used to control the sidebar state."""

    def __init__(self) -> None:
        """Initialize the sidebar state."""
        st.session_state.sidebar_state = "Hidden"

    def render_hidden_sidebar(self) -> None:
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

    def render_expanded_sidebar(self) -> None:
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

    def __call__(self, state: str = None) -> None:
        """Call the sidebar controller to render the sidebar.

        Args:
            state (str, optional): State that the sidebar should be rendered in. Defaults to None.

        """
        if state is None:

            if st.session_state.sidebar_state == "Hidden":
                self.render_hidden_sidebar()
            elif st.session_state.sidebar_state == "Expanded":
                self.render_expanded_sidebar()
            else:
                raise Exception("State not set and illdefined in session_state")

        elif state == "Expanded":
            self.render_expanded_sidebar()

        elif state == "Hidden":
            self.render_hidden_sidebar()
        else:
            raise Exception(
                f"State {state} recognized should be one of the following : [Exapnded, Hidden]"
            )

    def expand_sidebar(self) -> None:
        """Change the sidebar state to expanded."""
        st.session_state.sidebar_state = "Expanded"

    def hide_sidebar(self) -> None:
        """Change the sidebar state to hidden."""
        st.session_state.sidebar_state = "Hidden"


sidebar_controller = SideBarController()
