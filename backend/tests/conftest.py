"""This module contains fixtures for the tests."""
from functools import lru_cache

import pytest
from app import app
from database import BotsRepository, ConversationsRepository, Database, get_database
from fastapi.testclient import TestClient
from pymongo_inmemory import MongoClient


@lru_cache()
def get_mock_database():
    """Get the mock database in memory."""
    mongo_client = MongoClient()
    database = Database(
        bots=BotsRepository(mongo_client["bots"]),
        conversations=ConversationsRepository(mongo_client["conversations"]),
    )
    print("MOCK DATABASE CREATED!")
    return database


app.dependency_overrides[get_database] = get_mock_database


@pytest.fixture(scope="session")
def test_client():
    """Create a test client for the app."""
    with TestClient(app) as test_client:
        yield test_client