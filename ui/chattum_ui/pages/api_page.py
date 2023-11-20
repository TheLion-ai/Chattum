"""The dashboard page."""
from chattum_ui.templates import template

import reflex as rx
from chattum_ui.state import State
from settings import EXTERNAL_BACKEND_URL, USERNAME


@template(route="/api_page", title="API", image="/page_icons/api.svg")
def api_page() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.vstack(
        rx.text(State.bot_id),
        rx.html(
            f'<iframe src ="{EXTERNAL_BACKEND_URL}/docs/{USERNAME}/{State.get_bot_id}" width=800, height=1200px> </iframe>'
        ),
        width="100%",
        height="100%",
    )
