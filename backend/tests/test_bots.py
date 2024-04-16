"""Tests for the bots endpoints."""

import pytest
from bson import ObjectId


def test_create_bot(test_client, model_template) -> None:
    """Creates bot for testing."""
    global username
    global bot_id
    username = "test_user"
    bot_id = test_client.put(f"/{username}/bots", json=model_template).json()["bot_id"]


def test_get_bots(test_client, model_template) -> None:
    """Test the get bots endpoint."""
    response = test_client.get(f"/{username}/bots")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": bot_id,
            "tools": [],
            "sources": [],
            "prompt": "",
        }
        | model_template
    ]


def test_get_bots_not_found(test_client) -> None:
    """Test the get bots endpoint with a user that does not exist."""
    fake_username = "fake_user"
    response = test_client.get(f"/{fake_username}/bots")
    assert response.status_code == 200
    assert response.json() == []


def test_get_bot(test_client, model_template) -> None:
    """Test the get bot endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}")
    assert response.status_code == 200
    assert (
        response.json()
        == {
            "id": bot_id,
            "tools": [],
            "sources": [],
            "prompt": "",
        }
        | model_template
    )


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
