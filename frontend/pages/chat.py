"""Page for chatting with the bot."""
import streamlit as st
from streamlit_chat import message

from backend_controller import get_conversation

st.session_state.current_bot = st.experimental_get_query_params()["bot_id"][0]
bot_id = st.session_state.current_bot
messages = get_conversation(bot_id)

st.title("Chat")

for m in messages:
    is_user = m["type"] == "human"
    message(m["data"]["content"], is_user=is_user)
