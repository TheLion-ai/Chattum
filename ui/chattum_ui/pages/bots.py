"""The dashboard page."""
import reflex as rx
from chattum_ui.components.bots import bot_card, new_bot_modal
from chattum_ui.state import State
from chattum_ui.templates import template


@template(route="/", title="Bots", image="/page_icons/bots.svg")
def bots() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.button(
            "Add new bot",
            on_click=State.change_new_bot_modal_state,
        ),
        new_bot_modal(),
        rx.input(
            placeholder="Search",
            value=State.search_string,
            on_change=State.set_search_string,
        ),
        rx.responsive_grid(
            rx.foreach(
                State.bots,
                lambda bot: bot_card(bot),
            ),
            columns=[3],
            spacing="4",
        ),
    )
