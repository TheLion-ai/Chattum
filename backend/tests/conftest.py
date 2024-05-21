"""Fixtures for the tests."""

import os
from functools import lru_cache

import pytest
from app.database import get_mongo_client
from app.router import app
from fastapi.testclient import TestClient
from pymongo_inmemory import MongoClient


@lru_cache()
def get_mock_mongo_client():
    """Get the mock database in memory."""
    return MongoClient()


app.dependency_overrides[get_mongo_client] = get_mock_mongo_client

@pytest.fixture(scope="session")
def api_key():
    """Return the API key."""
    return os.getenv("API_KEY")

@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="session")
def model_template():
    """Return a model template."""
    return {
        "name": "test_bot",
        "username": "test_user",
        "model": {
            "name": "GPT",
            "id": None,
            "user_description": "OpenAI chat model",
            "user_variables": [
                {
                    "name": "model",
                    "description": "name of the model",
                    "value": "gpt-3.5-turbo",
                    "default_value": "gpt-3.5-turbo",
                    "form_type": "text",
                    "available_values": None,
                },
                {
                    "name": "openai_api_key",
                    "description": "your OpenAI API key",
                    "value": os.getenv("OPENAI_API_KEY"),
                    "default_value": None,
                    "form_type": "text",
                    "available_values": None,
                },
                {
                    "name": "temperature",
                    "description": "temperature for the model",
                    "value": 0.9,
                    "default_value": 0.9,
                    "form_type": "float",
                    "available_values": None,
                },
            ],
        },
    }
