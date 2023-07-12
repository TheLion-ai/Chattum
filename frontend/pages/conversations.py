"""Page for chatting with the bot."""
import streamlit as st
from streamlit_chat import message

from backend_controller import get_conversations


def show_conversation(conversation: dict) -> None:
    with conversation_content:
        for m in conversation["messages"]:
            is_user = m["type"] == "human"
            message(m["data"]["content"], is_user=is_user)


st.session_state.current_bot = st.experimental_get_query_params()["bot_id"][0]
bot_id = st.session_state.current_bot
conversations = get_conversations(bot_id)

st.title("Conversations")

conversation_buttons, conversation_content = st.columns([2, 3], gap="large")

with conversation_buttons:
    for conversation in conversations:
        st.button(
            conversation['id'],
            on_click=show_conversation,
            args=([conversation]),
            use_container_width=True,
        )
