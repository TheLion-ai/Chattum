"""The dashboard page."""
from chattum_ui.templates import template

import reflex as rx
from chattum_ui.state import State, ToolsState
from chattum_ui.components.tools import tool_form, tool_button, create_new_tool


@template(
    route="/tools",
    title="Tools",
    image="/page_icons/tools.svg",
    on_load=ToolsState.load_tools,
)
def tools() -> rx.Component:
    """The dashboard page.

    Returns:
        The UI for the dashboard page.
    """
    return rx.hstack(
        rx.box(
            rx.vstack(
                create_new_tool(),
                rx.foreach(
                    ToolsState.tools,
                    lambda tool: tool_button(tool),
                ),
                padding="10px",
            ),
            width="25%",
            overflow_y="scroll",
            height="100%",
        ),
        rx.box(
            rx.cond(
                ToolsState.tool != {},
                rx.cond(
                    ToolsState.tool_id,
                    tool_form(ToolsState.tool, ToolsState.user_variables),
                    rx.modal(
                        rx.modal_overlay(
                            rx.modal_content(
                                tool_form(ToolsState.tool, ToolsState.user_variables)
                            )
                        )
                    ),
                ),
            ),
            width="75%",
        ),
        height="80vh",
        align_items="flex-start",
    )
