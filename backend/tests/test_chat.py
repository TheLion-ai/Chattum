"""Tests for the chat endpoints."""


def test_create_bot(test_client) -> None:
    """Creates bot for testing."""
    global bot_id
    global username
    username = "test_user"
    bot_id = test_client.put(
        f"/{username}/bots", json={"name": "test_bot", "username": username}
    ).json()["bot_id"]


def test_put_prompt(test_client) -> None:
    """Test the put prompt endpoint."""
    response = test_client.put(
        f"/{username}/bots/{bot_id}/prompt",
        json={"prompt": "To every message, reply: 'Hello World!'"},
    )
    assert response.status_code == 200


def test_chat(test_client) -> None:
    """Test the chat endpoint."""
    global conversation_id
    response = test_client.post(
        f"/{username}/bots/{bot_id}/chat", json={"message": "hi"}
    )
    conversation_id = response.json()["conversation_id"]


def test_get_conversation(test_client) -> None:
    """Test that the chat is in conversation history."""
    response = test_client.get(
        f"/{username}/bots/{bot_id}/conversations/{conversation_id}"
    )
    assert response.status_code == 200
    messages = response.json()["messages"]
    assert messages[-2]["data"]["content"] == "hi"
    assert messages[-1]["data"]["content"] == "Hello World!"
