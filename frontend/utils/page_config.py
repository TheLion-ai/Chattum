"""Set the streamlit page config once."""

import streamlit as st


def set_streamlit_page_config_once() -> None:
    """Set the streamlit page config once."""
    try:
        st.set_page_config(layout="wide")
        st.set_page_config(
            page_title="Chattum",
            page_icon="🤖",
            layout="wide",
        )
    except st.errors.StreamlitAPIException as e:
        if "can only be called once per app" in e.__str__():
            # ignore this error
            return
        raise e


def ensure_bot_selected() -> None:
    if "bot_id" not in st.query_params:
        st.switch_page("🤖_bots.py")
