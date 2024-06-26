"""Test conversations endpoints."""

import pytest
from langchain.memory import ChatMessageHistory
from langchain.schema import messages_to_dict


def test_create_bot(test_client, model_template, api_key) -> None:
    """Set up the test client."""
    global username
    global bot_id
    username = "test_user"
    bot_id = test_client.put("/{username}/bots", json=model_template, headers={"X-API-Key": api_key}).json()["bot_id"]


def test_put_and_get(test_client, api_key) -> None:
    """Test put and get conversations endpoint."""
    # Create a sample conversation history with LangChain
    history = ChatMessageHistory()
    history.add_user_message("hi!")
    history.add_ai_message("whats up?")
    messages = messages_to_dict(history.messages)

    # Save history to database
    response = test_client.put(
        f"/{username}/bots/{bot_id}/conversations", json={"messages": messages}, headers={"X-API-Key": api_key}
    )
    conversation_id = response.json()["conversation_id"]

    # Get history from database
    response = test_client.get(
        f"/{username}/bots/{bot_id}/conversations/{conversation_id}", headers={"X-API-Key": api_key}
    )

    # Delete history from database
    test_client.delete(f"/{username}/bots/{bot_id}/conversations/{conversation_id}", headers={"X-API-Key": api_key})

    # Check if history is the same
    assert messages == response.json()["messages"]
