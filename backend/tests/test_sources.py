"""Tests for the sources endpoints."""

import pytest
from bson import ObjectId


def test_create_bot(test_client) -> None:
    """Creates bot for testing."""
    global bot_id
    global username
    username = "test_user"
    bot_id = test_client.put(
        f"/{username}/bots", json={"name": "test_bot", "username": username}
    ).json()["bot_id"]


def test_put_source(test_client) -> None:
    """Test the put source endpoint."""
    response = test_client.put(
        f"/{username}/bots/{bot_id}/sources", json={"source": "test_source"}
    )
    assert response.status_code == 200


def test_get_sources(test_client) -> None:
    """Test the get sources endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources")
    assert response.status_code == 200
    assert response.json() == {"sources": ["test_source"]}


def test_get_sources_not_found(test_client) -> None:
    """Test the get sources endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.get(f"/{username}/bots/{fake_id}/sources")
    assert response.status_code == 404


def test_delete_source(test_client) -> None:
    """Test the delete source endpoint."""
    response = test_client.delete(f"/{username}/bots/{bot_id}/sources/test_source")
    assert response.status_code == 200


def test_delete_source_not_found(test_client) -> None:
    """Test the delete source endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.delete(f"/{username}/bots/{fake_id}/sources/test_source")
    assert response.status_code == 404
