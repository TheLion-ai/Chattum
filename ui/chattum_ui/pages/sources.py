"""The dashboard page."""
from chattum_ui.templates import template

import reflex as rx
from chattum_ui.state import State, SourcesState
from chattum_ui.components.sources import source_button, source_card, add_new_source


@template(
    route="/sources",
    title="Sources",
    image="/page_icons/sources.svg",
    on_load=SourcesState.load_sources,
)
def sources() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.hstack(
        rx.box(
            rx.vstack(
                add_new_source(),
                rx.foreach(
                    SourcesState.sources,
                    lambda source: source_button(source),
                ),
                padding="10px",
            ),
            width="25%",
            overflow_y="scroll",
            height="100%",
        ),
        rx.box(
            rx.cond(
                SourcesState.source_id,
                source_card(
                    SourcesState.source,
                ),
            ),
            width="75%",
        ),
        height="80vh",
        align_items="flex-start",
    )
