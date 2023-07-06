"""Database module for the bots app."""
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from pydantic_models.bots import Bot
from pydantic_models.sources import Source
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient


class BotsRepository(AbstractRepository[Bot]):
    """Repository for bots."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "bots"


class SourcesRepository(AbstractRepository[Source]):
    """Repository for sources."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "sources"


@dataclass
class Database:
    """Database class."""

    bots: Optional[BotsRepository] = None
    sources: Optional[SourcesRepository] = None

    def init_repositories(self, mongo_client: MongoClient) -> None:
        """Create a database repositories from a mongo client."""
        self.bots = BotsRepository(mongo_client["bots"])
        self.sources = SourcesRepository(mongo_client["bots"])


@lru_cache()
def get_mongo_client() -> MongoClient:
    """Get the database."""
    return MongoClient(os.environ["MONGODB_URL"])
