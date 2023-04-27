import streamlit as st



class SideBarController():
    def __init__(self) -> None:
        if "sidebar_state" not in st.session_state:
            st.session_state.sidebar_state = "Hidden"
    
    def render_hidden_sidebar(self):
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"]{
                visibility: hidden;
            }
            """,
            unsafe_allow_html=True,
        )
    
    def render_expanded_sidebar(self):
        st.markdown(
            """
            <style>
            [data-testid="stSidebar"]{
                visibility: visible;
            }
            """,
            unsafe_allow_html=True,
        )
    
    def __call__(self, state : str = None):
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
            raise Exception(f"State {state} recognized should be one of the following : [Exapnded, Hidden]")
    
    def expand_sidebar(self):
        st.session_state.sidebar_state = "Expanded"
    def hide_sidebar(self):
        st.session_state.sidebar_state = "Hidden"
        
            
sidebar_controller = SideBarController()