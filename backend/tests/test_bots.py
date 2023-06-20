"""Tests for the bots endpoints."""

import pytest
from bson import ObjectId


def test_create_bot(test_client) -> None:
    """Creates bot for testing."""
    global username
    global bot_id
    username = "test_user"
    bot_id = test_client.put(
        f"/{username}/bots", json={"name": "test_bot", "username": "test_user"}
    ).json()["bot_id"]


def test_get_bots(test_client) -> None:
    """Test the get bots endpoint."""
    response = test_client.get(f"/{username}/bots")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": bot_id,
            "name": "test_bot",
            "username": "test_user",
            "tools": [],
            "sources": [],
            "prompt": "",
        }
    ]


def test_get_bots_not_found(test_client) -> None:
    """Test the get bots endpoint with a user that does not exist."""
    fake_username = "fake_user"
    response = test_client.get(f"/{fake_username}/bots")
    assert response.status_code == 200
    assert response.json() == []


def test_get_bot(test_client) -> None:
    """Test the get bot endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": bot_id,
        "name": "test_bot",
        "username": "test_user",
        "tools": [],
        "sources": [],
        "prompt": "",
    }


def test_get_bot_not_found(test_client) -> None:
    """Test the get bot endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.get(f"/{username}/bots/{fake_id}")
    assert response.status_code == 404


def test_delete_bot(test_client) -> None:
    """Test the delete bot endpoint."""
    response = test_client.delete(f"/{username}/bots/{bot_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Bot deleted successfully!"}
