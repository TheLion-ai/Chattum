import reflex as rx

from .state import State
from chattum_ui.utils import backend_controller as bc


class ChatState(State):
    conversation_id: str = None
    conversation: dict = {}

    new_message: str = ""
    waiting: bool = False

    def load_conversation(self, conversation_id: str) -> None:
        self.conversation_id = conversation_id
        self.conversation = bc.get_conversation(self.bot_id, conversation_id)
        print(self.conversation)

    async def send_message(self) -> None:
        self.waiting = True
        yield
        response, self.conversation_id = bc.send_message(
            self.bot_id, self.conversation_id, self.new_message
        )

        self.conversation = bc.get_conversation(self.bot_id, self.conversation_id)
        self.waiting = False

    @rx.var
    def messages(self) -> list[dict]:
        return [
            {"content": message["data"]["content"], "type": message["type"]}
            for message in self.conversation.get("messages", [])
        ]

    def set_new_message(self, new_message: str) -> None:
        self.new_message = new_message

    def start_new_conversation(self) -> None:
        self.conversation_id = None
        self.conversation = {}
        self.new_message = ""
