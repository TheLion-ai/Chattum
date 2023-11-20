"""Base state for the app."""
import json
from time import sleep
from typing import Optional

import reflex as rx
from chattum_ui.utils import backend_controller as bc


class State(rx.State):
    bot_id: str = None
    bot: dict = None

    prompt: str = ""
    prompt_updated: bool = False
    conversations: list[dict] = []
    search_string: str = ""

    new_bot_model_open: bool = False

    @rx.var
    def get_bot_id(self) -> str:
        return self.bot_id

    def load_bot(self, bot_id: str) -> None:
        self.bot_id = bot_id
        self.bot = bc.get_bot(bot_id)

    def load_conversations(self) -> None:
        self.conversations = bc.get_conversations(self.bot_id)

    def load_prompt(self) -> None:
        self.prompt = bc.get_prompt(self.bot_id)
        self.prompt_updated = False

    @rx.var
    def available_bots(self) -> list[dict]:
        return bc.get_bots()

    @rx.var
    def bots(self) -> list[dict]:
        if self.search_string is None == "":
            return self.available_bots
        return [
            bot
            for bot in self.available_bots
            if self.search_string in bot["name"].lower()
        ]

    @rx.var
    def get_bot_json(self) -> str:
        return json.dumps(self.bot, indent=4)

    def update_prompt(self) -> None:
        bc.create_new_prompt(self.prompt, self.bot_id)
        self.prompt_updated = True

    def change_new_bot_modal_state(self) -> None:
        self.new_bot_model_open = not self.new_bot_model_open

    def create_new_bot(self, form) -> None:
        bc.create_new_bot(form["bot_name"])
        self.change_new_bot_modal_state()
