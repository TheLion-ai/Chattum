import reflex as rx
from chattum_ui.utils import backend_controller as bc

from .state import State


class ConversationState(State):
    conversation_id: str = None
    conversation: dict = {}

    def load_conversation(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
        self.conversation = bc.get_conversation(self.bot_id, conversation_id)

    @rx.var
    def messages(self) -> list[dict]:
        return [
            {"content": message["data"]["content"], "type": message["type"]}
            for message in self.conversation.get("messages", [])
        ]
