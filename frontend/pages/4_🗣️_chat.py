"""Page for chatting with the bot."""

import streamlit as st
from backend_controller import get_conversation, send_message
from bson import ObjectId
from components.conversations import display_conversation
from components.sidebar import sidebar_controller
from utils import query_params
from utils.page_config import ensure_bot_or_workflow_selected
from components.authentication import protect_page

st.set_page_config(
    page_title="Chat | Chattum",
    page_icon="🗣️",
)

bot_id = query_params.get_from_url_or_state("bot_id")


ensure_bot_or_workflow_selected()
sidebar_controller()
protect_page()


if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ObjectId()
    st.session_state["conversation"] = []

col_1, col_2 = st.columns([4, 2])
with col_1:
    st.markdown(f"Conversation ID: `{st.session_state.conversation_id}`")
with col_2:
    clear_button = st.button(
        "Start new conversation", key="clear", use_container_width=True
    )
    if clear_button:
        st.session_state.conversation_id = ObjectId()
        st.session_state["conversation"] = []

chat_history_container = st.container()
input_container = st.container()
debug_container = st.container()

with input_container:
    # with st.form(key="chat_input", clear_on_submit=True):
    # user_input = st.text_area("Type your message:", key="input", height=100)
    # submit_button = st.form_submit_button(label="Send")
    user_input = st.chat_input("Type your message:", key="input")

    if user_input:
        input_container.empty()
        chat_history_container.empty()
        with st.spinner("Thinking..."):
            response = send_message(
                bot_id,
                st.session_state.conversation_id,
                user_input,
            )
            if response is not None:
                message, conversation_id = (
                    response["message"],
                    response["conversation_id"],
                )
                st.session_state.conversation_id = conversation_id
                st.session_state["conversation"] = get_conversation(
                    bot_id, st.session_state.conversation_id
                )

if st.session_state["conversation"]:
    with chat_history_container:
        display_conversation(st.session_state["conversation"])

with debug_container:
    with st.expander("Debug"):
        st.write(st.session_state["conversation"])
