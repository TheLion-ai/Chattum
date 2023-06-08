import unittest
from itertools import permutations

from app import app
from fastapi.testclient import TestClient
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict

# Remove the sorting of test methods
unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1


class TestConversations(unittest.TestCase):
    """Test conversations endpoint."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test client."""
        cls.test_client = TestClient(app)
        cls.bot_id = cls.test_client.put(
            "/bots", json={"name": "test_bot", "username": "test_user"}
        ).json()["bot_id"]

    def test_put_and_get(self) -> None:
        """Test put and get conversations endpoint """

        # Create a sample conversation history with LangChain
        history = ChatMessageHistory()
        history.add_user_message("hi!")
        history.add_ai_message("whats up?")
        messages = messages_to_dict(history.messages)

        # Save history to database
        response = self.test_client.put(f"/bots/{self.bot_id}/conversations", json={"messages": messages})
        conversation_id = response.json()['conversation_id']

        # Get history from database
        response = self.test_client.get(f"/bots/{self.bot_id}/conversations/{conversation_id}")

        # Delete history from database
        self.test_client.delete(f"/bots/{self.bot_id}/conversations/{conversation_id}")

        # Check if history is the same
        assert messages == response.json()['messages']


if __name__ == "__main__":
    unittest.main()
