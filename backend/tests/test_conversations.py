"""Test conversations endpoints."""
import pytest
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict


def test_create_bot(test_client) -> None:
    """Set up the test client."""
    global username
    global bot_id
    username = "test_user"
    bot_id = test_client.put(
        "/{username}/bots", json={"name": "test_bot", "username": "test_user"}
    ).json()["bot_id"]


def test_put_and_get(test_client) -> None:
    """Test put and get conversations endpoint."""
    # Create a sample conversation history with LangChain
    history = ChatMessageHistory()
    history.add_user_message("hi!")
    history.add_ai_message("whats up?")
    messages = messages_to_dict(history.messages)

    # Save history to database
    response = test_client.put(
        f"/{username}/bots/{bot_id}/conversations", json={"messages": messages}
    )
    conversation_id = response.json()["conversation_id"]

    # Get history from database
    response = test_client.get(
        f"/{username}/bots/{bot_id}/conversations/{conversation_id}"
    )

    # Delete history from database
    test_client.delete(f"/{username}/bots/{bot_id}/conversations/{conversation_id}")

    # Check if history is the same
    assert messages == response.json()["messages"]
