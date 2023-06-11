"""Functions exchanging information from frontend with backend."""
from typing import List

import requests
import streamlit as st
from langchain.memory import ChatMessageHistory

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


def create_new_prompt(prompt: str, bot_id: str) -> None:
    """Create a new prompt based on text from text area."""
    try:
        response = requests.put(
            f"{BACKEND_URL}/bots/{bot_id}/prompt", json={"prompt": prompt}
        )
        if response.status_code == 200:
            st.success("Prompt created", icon="👍")
        else:
            raise Exception(f"error: {response.status_code} {response.text}")
    except Exception as e:
        st.warning(e)


def get_prompt(bot_id: str) -> str:
    """Get the current prompt of a bot.

    Returns:
        str: bot's prompt.
    """
    prompt = requests.get(f"{BACKEND_URL}/bots/{bot_id}/prompt").json()["prompt"]

    return prompt


def get_conversation(bot_id: str) -> List[dict]:
    try:
        messages = requests.get(f"{BACKEND_URL}/bots/{bot_id}/conversations").json()[0]["messages"]
    except IndexError:
        messages = []
    return messages
