"""Functions exchanging information from frontend with backend."""
import requests
import streamlit as st
from constants import BACKEND_URL, USERNAME


def get_bots() -> list[dict]:
    """Get a list of available bots.

    Returns:
        list[dict]: a list of created bots.
    """
    bots = requests.get(f"{BACKEND_URL}/bots", json={"username": USERNAME}).json()

    return bots


def create_new_bot(bot_name: str) -> None:
    """Create a new bot with a given name.

    Args:
        bot_name (str): a name for a new bot
    """
    try:
        response = requests.put(
            f"{BACKEND_URL}/bots", json={"name": bot_name, "username": USERNAME}
        )
        assert response.status_code == 200
        st.success(f"Bot {bot_name} created")
    except Exception as e:
        st.warning(e)
