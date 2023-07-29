"""Page for chatting with the bot."""
import streamlit as st
from backend_controller import get_conversation, send_message
from bson import ObjectId
from components.conversations import display_conversation
from utils import query_params


def render_chat() -> None:
    """Page for chatting with the bot."""
    current_bot = query_params.get_form_url("bot_id")

    if "conversation_id" not in st.session_state:
        st.session_state.conversation_id = ObjectId()

    st.session_state["conversation"] = get_conversation(
        current_bot, st.session_state.conversation_id
    )

    col_1, col_2 = st.columns(2)
    with col_1:
        st.markdown(f"Conversation ID: `{st.session_state.conversation_id}`")
    with col_2:
        clear_button = st.button("Start new conversation", key="clear")
        if clear_button:
            st.session_state.conversation_id = ObjectId()
            st.session_state["conversation"] = get_conversation(
                current_bot, st.session_state.conversation_id
            )

    chat_history_container = st.container()
    input_container = st.container()
    debug_container = st.container()

    with input_container:
        with st.form(key="chat_input", clear_on_submit=True):
            user_input = st.text_area("Type your message:", key="input", height=100)
            submit_button = st.form_submit_button(label="Send")

        if submit_button and user_input:
            input_container.empty()
            chat_history_container.empty()
            with st.spinner("Thinking..."):
                response, conversation_id = send_message(
                    current_bot,
                    st.session_state.conversation_id,
                    user_input,
                )
                st.session_state.conversation_id = conversation_id
                st.session_state["conversation"] = get_conversation(
                    current_bot, st.session_state.conversation_id
                )

    if st.session_state["conversation"]:
        with chat_history_container:
            display_conversation(st.session_state["conversation"])

    with debug_container:
        with st.expander("Debug"):
            st.write(st.session_state["conversation"])
