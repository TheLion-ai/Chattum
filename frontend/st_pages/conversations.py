"""Page for chatting with the bot."""
import streamlit as st
from backend_controller import get_conversations
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

            for conversation in conversations:
                st.button(
                    conversation["id"],
                    use_container_width=True,
                    on_click=query_params.set_to_url,
                    kwargs={"conversation_id": conversation["id"]},
                    type="primary"
                    if conversation_id == conversation["id"]
                    else "secondary",
                )

    with conversation_content_container:
        if current_conversation:
            for i, m in enumerate(current_conversation["messages"]):
                is_user = m["type"] == "human"
                message(
                    m["data"]["content"],
                    is_user=is_user,
                    key=f"{current_conversation['id']}-{i}",
                )
