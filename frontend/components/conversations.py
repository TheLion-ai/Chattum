"""Streamlit component to display a conversation."""

import random

from streamlit_chat import message


def display_conversation(conversation: dict) -> None:
    """Show a conversation."""
    for m in conversation["messages"]:
        if m["type"] == "human":
            message(m["data"]["content"], is_user=True, key=str(random.random()))
        elif m["type"] == "ai":
            message(m["data"]["content"], is_user=False, key=str(random.random()))
