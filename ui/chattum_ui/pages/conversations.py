"""The dashboard page."""
import reflex as rx
from chattum_ui.components.conversations import conversation_button, show_conversation
from chattum_ui.state import ConversationState, State
from chattum_ui.templates import template


@template(
    route="/conversations",
    title="Conversations",
    on_load=State.load_conversations,
    image="/page_icons/conversations.svg",
)
def conversations(conversation_id=None) -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.hstack(
        rx.box(
            rx.vstack(
                rx.foreach(
                    State.conversations,
                    lambda conversation: conversation_button(conversation),
                ),
                padding="10px",
            ),
            width="25%",
            overflow_y="scroll",
            height="100%",
        ),
        rx.box(
            rx.cond(
                ConversationState.conversation_id,
                show_conversation(
                    ConversationState.conversation, ConversationState.messages
                ),
            ),
            width="75%",
        ),
        height="80vh",
        align_items="flex-start",
    )
