"""Fixtures for the tests."""
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
def test_client():
    """Create a test client for the app."""
    with TestClient(app) as test_client:
        yield test_client
