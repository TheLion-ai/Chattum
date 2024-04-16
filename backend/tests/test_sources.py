"""Tests for the sources endpoints."""

import filecmp

import pytest
from bson import ObjectId


def test_create_bot(test_client, model_template) -> None:
    """Creates bot for testing."""
    global bot_id
    global username
    username = "test_user"
    response = test_client.put(f"/{username}/bots", json=model_template)
    bot_id = response.json()["bot_id"]


def test_put_source_pdf(test_client) -> None:
    """Test the put source endpoint."""
    global source_id_pdf

    with open("tests/files/sample.pdf", "rb") as file:
        response = test_client.put(
            f"/{username}/bots/{bot_id}/sources",
            params={
                "name": "sample_pdf",
                "source_type": "pdf",
            },
            files={"file": file},  # type: ignore
        )
        source_id_pdf = response.json()["source_id"]
        assert response.status_code == 200


def test_put_source_url(test_client) -> None:
    """Test the put source endpoint."""
    global source_id_url

    response = test_client.put(
        f"/{username}/bots/{bot_id}/sources",
        params={
            "name": "sample_url",
            "source_type": "url",
            "url": "https://httpbin.org/html",
        },
    )
    source_id_url = response.json()["source_id"]
    assert response.status_code == 200


def test_get_sources(test_client) -> None:
    """Test the get sources endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources")
    assert response.status_code == 200
    assert response.json()["sources"] == [
        {"name": "sample_pdf", "source_type": "pdf", "id": source_id_pdf},
        {"name": "sample_url", "source_type": "url", "id": source_id_url},
    ]


def test_get_source_pdf(test_client) -> None:
    """Test the get source endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources/{source_id_pdf}")
    assert response.status_code == 200
    print("RESPONSE", response.json())
    print("SOURCEID", {"id": source_id_pdf, "name": "sample", "source_type": "pdf"})
    assert response.json() == {
        "id": source_id_pdf,
        "name": "sample_pdf",
        "source_type": "pdf",
    }

    response = test_client.get(
        f"/{username}/bots/{bot_id}/sources/{source_id_pdf}/file"
    )
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


def test_get_source_url(test_client) -> None:
    """Test the get source endpoint."""
    response = test_client.get(f"/{username}/bots/{bot_id}/sources/{source_id_url}")
    assert response.status_code == 200
    print("RESPONSE", response.json())
    print("SOURCEID", {"id": source_id_url, "name": "sample", "source_type": "url"})
    assert response.json() == {
        "id": source_id_url,
        "name": "sample_url",
        "source_type": "url",
    }

    response = test_client.get(
        f"/{username}/bots/{bot_id}/sources/{source_id_url}/file"
    )
    try:
        with open("tests/files/sample_url_downloaded.txt", "wb") as f:
            f.write(response.content)
        assert filecmp.cmp(
            "tests/files/sample_url.txt", "tests/files/sample_url_downloaded.txt"
        )
    except AssertionError:
        raise AssertionError("File not downloaded correctly")
    finally:
        import os

        if os.path.exists("tests/files/sample_url_downloaded.txt"):
            os.remove("tests/files/sample_url_downloaded.txt")


def test_get_sources_not_found(test_client, id="123456789012345678901234") -> None:
    """Test the get sources endpoint with a bot that does not exist."""
    fake_id = ObjectId(id)
    response = test_client.get(f"/{username}/bots/{fake_id}/sources")
    assert response.status_code == 404
    assert response.json() == {"detail": "Bot not found"}


def test_delete_source_pdf(test_client) -> None:
    """Test the delete source endpoint."""
    response = test_client.delete(f"/{username}/bots/{bot_id}/sources/{source_id_pdf}")
    assert response.status_code == 200
    test_get_sources_not_found(test_client, source_id_pdf)


def test_delete_source_not_found(test_client) -> None:
    """Test the delete source endpoint with a bot that does not exist."""
    fake_id = ObjectId("123456789012345678901234")
    response = test_client.delete(f"/{username}/bots/{fake_id}/sources/{source_id_pdf}")
    assert response.status_code == 404


def test_delete_source_url(test_client) -> None:
    """Test the delete source endpoint."""
    response = test_client.delete(f"/{username}/bots/{bot_id}/sources/{source_id_url}")
    assert response.status_code == 200
    test_get_sources_not_found(test_client, source_id_url)
