"""Tests for the backend application."""
import unittest
from itertools import permutations

from app import app
from bson import ObjectId
from fastapi.testclient import TestClient

# Remove the sorting of test methods
unittest.TestLoader.sortTestMethodsUsing = lambda *args: -1


class TestPrompts(unittest.TestCase):
    """Test the prompt endpoints."""

    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test client."""
        cls.test_client = TestClient(app)
        cls.bot_id = cls.test_client.put(
            "/bots", json={"name": "test_bot", "username": "test_user"}
        ).json()["bot_id"]

    def test_put_prompt(self) -> None:
        """Test the put prompt endpoint."""
        response = self.test_client.put(
            f"/bots/{self.bot_id}/prompt", json={"prompt": "Hello World!"}
        )
        print("PUT PROMPT")
        assert response.status_code == 200

    def test_get_prompt(self) -> None:
        """Test the get prompt endpoint."""
        response = self.test_client.get(f"/bots/{self.bot_id}/prompt")
        assert response.status_code == 200
        assert response.json() == {"prompt": "Hello World!"}

    def test_get_prompt_not_found(self) -> None:
        """Test the get prompt endpoint with a bot that does not exist."""
        fake_id = ObjectId("123456789012345678901234")
        response = self.test_client.get(f"/bots/{fake_id}/prompt")
        assert response.status_code == 404

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test client and delete the bot."""
        cls.test_client.delete(f"/bots/{cls.bot_id}")
        return super().tearDown(cls)


if __name__ == "__main__":
    unittest.main()
