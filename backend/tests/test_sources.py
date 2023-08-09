"""Tests for the sources endpoints."""

import filecmp

import pytest
from bson import ObjectId


def test_create_bot(test_client) -> None:
    """Creates bot for testing."""
    global bot_id
    global username
    username = "test_user"
    response = test_client.put(
        f"/{username}/bots", json={"name": "test_bot", "username": username}
    )
    bot_id = response.json()["bot_id"]


def test_put_source(test_client) -> None:
    """Test the put source endpoint."""
    global source_id

    with open("tests/files/sample.pdf", "rb") as file:
        response = test_client.put(
            f"/{username}/bots/{bot_id}/sources",
            data={"name": "sample", "source_type": "pdf"},
            files={"file": file},
        )
        source_id = response.json()["source_id"]
        assert response.status_code == 200


def test_get_sources(test_client) -> None:
    """Test the get sources endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources")
    assert response.status_code == 200
    assert response.json() == [
        {"name": "sample", "source_type": "pdf", "id": source_id}
    ]


def test_get_source(test_client) -> None:
    """Test the get source endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources/{source_id}")
    assert response.status_code == 200
    assert response.json() == {"id": source_id, "name": "sample", "source_type": "pdf"}

    response = test_client.get(f"/{username}/bots/{bot_id}/sources/{source_id}/file")
    try:
        with open("tests/files/sample_downloaded.pdf", "wb") as f:
            f.write(response.content)
        assert filecmp.cmp(
            "tests/files/sample.pdf", "tests/files/sample_downloaded.pdf"
        )
    except AssertionError:
        raise AssertionError("File not downloaded correctly")
    finally:
        import os

        if os.path.exists("tests/files/sample_downloaded.pdf"):
            os.remove("tests/files/sample_downloaded.pdf")


def test_get_sources_not_found(test_client, id="123456789012345678901234") -> None:
    """Test the get sources endpoint with a bot that does not exist."""
    fake_id = ObjectId(id)
    response = test_client.get(f"/{username}/bots/{fake_id}/sources")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bot not found"}


def test_delete_source(test_client) -> None:
    """Test the delete source endpoint."""
    response = test_client.delete(f"/{username}/bots/{bot_id}/sources/{source_id}")
    assert response.status_code == 200
    test_get_sources_not_found(test_client, source_id)


def test_delete_source_not_found(test_client) -> None:
    """Test the delete source endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.delete(f"/{username}/bots/{fake_id}/sources/{source_id}")
    assert response.status_code == 404
