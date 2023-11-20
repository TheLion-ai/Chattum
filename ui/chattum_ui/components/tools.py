import reflex as rx
from chattum_ui import styles
from chattum_ui.state import State, ToolsState


def tool_button(tool: dict) -> rx.Component:
    active = tool["id"] == ToolsState.tool_id

    return rx.card(
        tool["id"],
        on_click=ToolsState.load_tool(tool["id"]),
        align_self="baseline",
        width="100%",
        bg=rx.cond(active, styles.secondary_color, "transparent"),
        border_radius=styles.border_radius,
        box_shadow=styles.box_shadow,
        _hover={"cursor": "pointer", "color": styles.accent_color},
    )


def tool_form(tool: dict, user_variables) -> rx.Component:
    return rx.vstack(
        rx.heading(tool["name"]),
        rx.text(tool["user_description"]),
        rx.foreach(user_variables, lambda variable: user_variable_form(variable)),
        rx.cond(
            ToolsState.creating_new_tool,
            rx.flex(
                rx.button(
                    "Create tool",
                    on_click=ToolsState.update_tool,
                    # disable=~ToolsState.variables_changed,
                ),
                rx.spacer(),
                rx.button(
                    "Cancel",
                    on_click=ToolsState.toggle_creating_new_tool,
                    # color_scheme="red",
                    # variant="outline",
                ),
                width="100%",
            ),
            rx.flex(
                rx.button(
                    "Update tool",
                    on_click=ToolsState.update_tool,
                    is_disabled=~ToolsState.variables_changed,
                ),
                rx.spacer(),
                rx.button(
                    "Delete tool",
                    on_click=ToolsState.delete_tool,
                    color_scheme="red",
                    variant="outline",
                ),
                width="80%",
            ),
        ),
        on_unmount=lambda: ToolsState.load_user_variables(),
        width="100%",
    )


def user_variable_form(variable: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            rx.heading(variable.name, font_size="1.5em"),
            rx.text(variable.description),
            rx.cond(
                variable.form_type == "text",
                rx.input(
                    value=variable.value,
                    on_change=lambda value: ToolsState.update_user_variable(
                        variable.name, value
                    ),
                    width="100%",
                    # on_unmount=lambda: ToolsState.update_user_variable(
                    #     variable.name, ""
                    # ),
                ),
            ),
            rx.cond(
                variable.form_type == "editor",
                rx.text_area(
                    value=variable.value,
                    on_change=lambda value: ToolsState.update_user_variable(
                        variable.name, value
                    ),
                    width="100%",
                ),
            ),
        ),
        width=rx.cond(ToolsState.creating_new_tool, "100%", "80%"),
        box_shadow=styles.box_shadow,
    )


def create_new_tool() -> rx.Component:
    return rx.box(
        rx.button("Add new tool", on_click=ToolsState.toggle_creating_new_tool),
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header(
                        rx.heading("Add new tool"),
                    ),
                    rx.modal_body(
                        rx.vstack(
                            rx.select(
                                ToolsState.available_tools_names,
                                placeholder="Select tool type",
                                on_change=ToolsState.set_new_tool_name,
                            ),
                            rx.cond(
                                ToolsState.new_tool_name,
                                rx.vstack(
                                    rx.text(
                                        ToolsState.new_tool_description, margin="10px"
                                    ),
                                    tool_form(
                                        ToolsState.tool, ToolsState.user_variables
                                    ),
                                    width="100%",
                                ),
                            ),
                        ),
                        width="100%",
                    ),
                    width="100%",
                ),
                width="100%",
            ),
            size="2xl",
            is_open=ToolsState.creating_new_tool,
        ),
    )
