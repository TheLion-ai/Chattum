"""Database module for the bots app."""
import os
from collections import namedtuple
from functools import lru_cache

from pydantic import BaseModel
from pydantic_models.bots import Bot
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient

Database = namedtuple("Database", ["bots"])


class BotsRepository(AbstractRepository[Bot]):
    """Repository for bots."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "bots"


def create_repositories(mongo_client: MongoClient) -> Database:
    """Create repositories."""
    return Database(bots=BotsRepository(mongo_client["bots"]))


@lru_cache()
def get_database() -> Database:
    """Get the database."""
    mongo_client = MongoClient(os.environ["MONGODB_URL"])
    database = create_repositories(mongo_client)
    return database
