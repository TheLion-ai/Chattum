"""The settings page."""

from chattum_ui.templates import template
import json
import reflex as rx
from chattum_ui.state import State


@template(route="/settings", title="Settings", image="/page_icons/settings.svg")
def settings() -> rx.Component:
    return rx.code_block(State.get_bot_json, language="json")
