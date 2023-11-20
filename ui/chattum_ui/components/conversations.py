import reflex as rx
from chattum_ui import styles
from chattum_ui.state import ConversationState, State


def conversation_button(conversation) -> rx.Component:
    active = conversation["id"] == ConversationState.conversation_id

    return rx.card(
        conversation["id"],
        on_click=ConversationState.load_conversation(conversation["id"]),
        align_self="baseline",
        width="100%",
        bg=rx.cond(active, styles.secondary_color, "transparent"),
        border_radius=styles.border_radius,
        box_shadow=styles.box_shadow,
        _hover={"cursor": "pointer", "color": styles.accent_color},
    )


def show_conversation(conversation, messages: list) -> rx.Component:
    return rx.cond(
        messages != [],
        rx.vstack(
            rx.foreach(
                messages,
                lambda message: show_message(message),
            ),
            width="100%",
        ),
    )


def show_message(message: dict) -> rx.Component:
    return rx.cond(
        message["type"] == "human",
        human_message(message["content"]),
        bot_message(message["content"]),
    )


def human_message(message: str) -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.text(message),
            rx.avatar(
                src="https://api.dicebear.com/7.x/avataaars-neutral/svg?seed=Gizmo&backgroundColor=edb98a,ffdbb4,d1d4f9&backgroundType[]&eyebrows=default&eyes=eyeRoll,surprised,squint,default&mouth=default,smile,twinkle"
            ),
            border_radius=styles.border_radius,
            box_shadow=styles.box_shadow,
            padding="10px",
            margin_right=0,
            margin_left="auto",
            justify_content="flex-end",
        ),
        width="100%",
    )


def bot_message(message: str) -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.avatar(
                name="A I",
                src="https://api.dicebear.com/7.x/bottts/svg?seed=Sam&baseColor=1e88e5,039be5&eyes=glow&face=square01&mouth=smile01&sides=antenna02,cables01,cables02,round,square,squareAssymetric&textureProbability=0&backgroundColor=transparent",
            ),
            rx.text(message),
            border_radius=styles.border_radius,
            box_shadow=styles.box_shadow,
            padding="10px",
            width="80%",
        ),
        rx.box(width="20%"),
        width="100%",
    )
