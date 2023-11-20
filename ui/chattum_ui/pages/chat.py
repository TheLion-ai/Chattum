"""The dashboard page."""
import reflex as rx
from chattum_ui.components.conversations import conversation_button, show_conversation
from chattum_ui.state import ChatState, State
from chattum_ui.templates import template


@template(route="/chat", title="Chat", image="/page_icons/chat.svg")
def chat() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.text(ChatState.conversation_id),
        rx.cond(
            ChatState.conversation_id,
            show_conversation(ChatState.conversation, ChatState.messages),
        ),
        rx.cond(ChatState.waiting, rx.spinner(size="xl")),
        rx.hstack(
            rx.text_area(
                ChatState.new_message,
                placeholder="Enter message here",
                width="80%",
                on_change=lambda x: ChatState.set_new_message(x),
            ),
            rx.vstack(
                rx.button("Send", on_click=ChatState.send_message, width="100%"),
                rx.button(
                    "Start New Conversation",
                    on_click=ChatState.start_new_conversation,
                    width="100%",
                ),
                width="20%",
            ),
            width="100%",
        ),
    )
