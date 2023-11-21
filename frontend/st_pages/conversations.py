"""Page for chatting with the bot."""
import math
from datetime import datetime

import streamlit as st
from backend_controller import get_conversations
from components.conversations import display_conversation
from streamlit_chat import message
from utils import query_params


def render_conversations() -> None:
    """Page for viewing conversations."""
    current_bot = query_params.get_form_url("bot_id")
    conversation_id = query_params.get_form_url("conversation_id")

    conversations = get_conversations(current_bot)

    current_conversation = next(
        (x for x in conversations if x["id"] == conversation_id), None
    )

    st.title("Conversations")
    conversation_list, conversation_content = st.columns([3, 5], gap="large")
    with conversation_list:
        conversation_list_container = st.container()
    with conversation_content:
        conversation_content_container = st.container()

    with conversation_list_container:
        if conversations == []:
            st.write("No conversations yet!")
        else:
            st.write("Click on a conversation to view it!")

            # Sort conversations by timestamp
            conversations = sorted(
                conversations,
                key=lambda x: x.get("last_message_time")
                if x.get("last_message_time") is not None
                else "",
                reverse=True,
            )

            for conversation in conversations:
                # Reformat the date
                format_1 = "%Y-%m-%dT%H:%M:%S.%f"
                format_2 = "%d/%m/%Y %H:%M:%S"
                last_message_time_str = (
                    datetime.strptime(
                        conversation["last_message_time"], format_1
                    ).strftime(format_2)
                    if conversation.get("last_message_time") is not None
                    else ""
                )

                st.button(
                    last_message_time_str,
                    use_container_width=True,
                    on_click=query_params.set_to_url,
                    kwargs={"conversation_id": conversation["id"]},
                    type="primary"
                    if conversation_id == conversation["id"]
                    else "secondary",
                    key=conversation["id"],
                )

    with conversation_content_container:
        if current_conversation:
            display_conversation(current_conversation)
