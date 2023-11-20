import reflex as rx
from chattum_ui import styles
from chattum_ui.state import State


def bot_card(bot: dict) -> rx.Component:
    """A card for a bot.

    Args:
        bot: The bot to display.

    Returns:
        The UI for the bot card.
    """

    selected = State.bot_id == bot["id"]

    return rx.card(
        rx.vstack(
            # rx.text(bot["tools"].length()),
            # rx.image(
            #     src=f"https://api.dicebear.com/7.x/bottts/svg?eyes=frame1,frame2&baseColor=039be5&seed={bot['id']}",
            #     width="30%",
            # ),
            rx.text(bot["prompt"]),
        ),
        header=rx.heading(bot["name"], font_size="1.5em"),
        footer=rx.button(
            "Select",
            on_click=State.load_bot(bot["id"]),
            # bg=styles.accent_color,
        ),
        bg=rx.cond(selected, styles.secondary_color, "transparent"),
        # border=rx.cond(
        #     State.bot_id == bot["id"],
        #     f"2px solid {styles.primary_color}",
        #     "2px solid #FFFFFF",
        # ),
    )


def new_bot_modal() -> rx.Component:
    """A modal for creating a new bot.

    Returns:
        The UI for the new bot modal.
    """
    return rx.modal(
        rx.modal_overlay(
            rx.modal_content(
                rx.modal_header(
                    rx.heading("Create a new bot"),
                ),
                rx.modal_body(
                    rx.vstack(
                        rx.text("Give your bot a name"),
                        rx.form(
                            rx.vstack(
                                rx.input(
                                    placeholder="Bot name",
                                    id="bot_name",
                                ),
                            ),
                            rx.flex(
                                rx.button("Create bot", type_="submit"),
                                rx.spacer(),
                                rx.button(
                                    "Cancel", on_click=State.change_new_bot_modal_state
                                ),
                                width="100%",
                                margin_top="20px",
                            ),
                            on_submit=State.create_new_bot,
                        ),
                    ),
                ),
            ),
        ),
        is_open=State.new_bot_model_open,
    )
