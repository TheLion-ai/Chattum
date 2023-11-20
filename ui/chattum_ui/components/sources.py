import reflex as rx
from chattum_ui import styles
from chattum_ui.state import NewSourceState, SourcesState, State


def source_button(source) -> rx.Component:
    active = source["id"] == SourcesState.source_id
    return rx.card(
        rx.hstack(
            rx.text(source["name"]),
            rx.badge(source["source_type"], color=styles.accent_color),
        ),
        on_click=SourcesState.load_source(source["id"]),
        align_self="baseline",
        width="100%",
        _hover={"color": styles.accent_color, "cursor": "pointer"},
        bg=rx.cond(active, styles.secondary_color, "transparent"),
        border_radius=styles.border_radius,
        box_shadow=styles.box_shadow,
    )


def source_card(source: dict) -> rx.Component:
    """A card for a bot.

    Args:
        bot: The bot to display.

    Returns:
        The UI for the bot card.
    """
    return rx.card(
        source["id"],
        header=rx.heading(source["name"], font_size="1.5em"),
        footer=rx.flex(
            rx.button("Download", on_click=SourcesState.download_source(source["id"])),
            rx.spacer(),
            rx.button("Delete", on_click=SourcesState.delete_source(source["id"])),
            width="100%",
        ),
    )


def add_new_source():
    return rx.box(
        rx.button("Add new source", on_click=NewSourceState.change_modal_state),
        rx.modal(
            rx.modal_overlay(
                rx.modal_content(
                    rx.modal_header(
                        rx.heading("Add new source"),
                    ),
                    rx.modal_body(
                        rx.form(
                            rx.vstack(
                                rx.form_control(
                                    rx.select(
                                        NewSourceState.valid_file_types,
                                        placeholder="Select source type",
                                        id="source_type",
                                        margin_bottom="10px",
                                        on_change=lambda value: NewSourceState.set_source_type(
                                            value
                                        ),
                                    ),
                                    rx.cond(
                                        NewSourceState.source_type_valid,
                                        rx.form_error_message(
                                            "Select a valid source type"
                                        ),
                                    ),
                                    is_invalid=~NewSourceState.source_type_valid,
                                ),
                                rx.spacer(),
                                rx.input(
                                    placeholder="Enter source name",
                                    id="source_name",
                                    margin_bottom="10px",
                                    on_blur=lambda value: NewSourceState.set_source_name(
                                        value
                                    ),
                                ),
                                rx.spacer(),
                                rx.cond(
                                    NewSourceState.source_type == "url",
                                    rx.input(
                                        placeholder="Enter source url",
                                        id="source_url",
                                        margin_bottom="10px",
                                        on_blur=lambda value: NewSourceState.set_source_url(
                                            value
                                        ),
                                    ),
                                    rx.box(
                                        rx.upload(
                                            rx.cond(
                                                rx.selected_files,
                                                rx.text(rx.selected_files),
                                                rx.text(
                                                    "Drag and drop files here or click to select files"
                                                ),
                                                # rx.button("Upload"),
                                            ),
                                            border="1px dotted rgb(107,99,246)",
                                            padding="2em",
                                            id="source_file",
                                        ),
                                        rx.cond(
                                            rx.selected_files,
                                            rx.button(
                                                rx.cond(
                                                    NewSourceState.source_file_valid,
                                                    "File uploaded",
                                                    "Upload",
                                                ),
                                                on_click=lambda: NewSourceState.set_source_file(
                                                    rx.upload_files()
                                                ),
                                                width="100%",
                                                is_disabled=NewSourceState.source_file_valid,
                                            ),
                                        ),
                                        width="100%",
                                    ),
                                ),
                                rx.flex(
                                    rx.button(
                                        "Submit",
                                        type_="submit",
                                        is_disabled=~NewSourceState.form_valid,
                                    ),
                                    rx.spacer(),
                                    rx.button(
                                        "Cancel",
                                        on_click=NewSourceState.change_modal_state,
                                    ),
                                    width="100%",
                                ),
                            ),
                            on_submit=NewSourceState.add_new_source,
                        ),
                        rx.cond(
                            NewSourceState.adding_in_progress,
                            rx.progress(is_indeterminate=True, width="100%"),
                        ),
                    ),
                )
            ),
            is_open=NewSourceState.modal_opened,
        ),
    )
