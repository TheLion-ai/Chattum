"""Tests for the backend application."""

import pytest
from bson import ObjectId


def test_create_bot(test_client) -> None:
    """Creates bot for testing."""
    global bot_id
    bot_id = test_client.put(
        "/bots", json={"name": "test_bot", "username": "test_user"}
    ).json()["bot_id"]


def test_put_prompt(test_client) -> None:
    """Test the put prompt endpoint."""
    response = test_client.put(
        f"/bots/{bot_id}/prompt", json={"prompt": "Hello World!"}
    )
    assert response.status_code == 200


def test_get_prompt(test_client) -> None:
    """Test the get prompt endpoint."""
    response = test_client.get(f"/bots/{bot_id}/prompt")
    assert response.status_code == 200
    assert response.json() == {"prompt": "Hello World!"}


def test_get_prompt_not_found(test_client) -> None:
    """Test the get prompt endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.get(f"/bots/{fake_id}/prompt")
    assert response.status_code == 404
