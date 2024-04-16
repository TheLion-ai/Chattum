"""Streamlit component to display a conversation."""

import random

import streamlit as st
from streamlit_chat import message


def display_conversation(conversation: dict) -> None:
    """Show a conversation."""
    for m in conversation["messages"]:
        if m["type"] == "human":
            with st.chat_message("user"):
                st.write(m["data"]["content"])
            # message(m["data"]["content"], is_user=True, key=str(random.random()))
        elif m["type"] == "ai":
            with st.chat_message("assistant"):
                st.write(m["data"]["content"])
                if "tool_calls" in m["data"] and m["data"]["tool_calls"] != []:
                    col1, col2 = st.columns([4, 4])
                    with col2:
                        for tool in m["data"]["tool_calls"]:
                            with st.expander(f"Tool used: {tool['name']}"):
                                st.write(tool["args"])
            # message(m["data"]["content"], is_user=False, key=str(random.random()))
