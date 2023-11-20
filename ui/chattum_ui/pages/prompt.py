"""The dashboard page."""
import reflex as rx
from chattum_ui.components.bots import bot_card
from chattum_ui.state import State
from chattum_ui.templates import template


@template(
    route="/prompt",
    title="prompt",
    on_load=State.load_prompt,
    image="/page_icons/prompt.svg",
)
def prompt() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.cond(
            State.prompt_updated,
            rx.alert(
                rx.alert_icon(),
                rx.alert_title("Prompt updated"),
                status="success",
            ),
        ),
        rx.text_area(
            value=State.prompt,
            placeholder="Enter prompt here",
            on_change=State.set_prompt,
        ),
        rx.button(
            "Submit",
            on_click=State.update_prompt,
        ),
    )
