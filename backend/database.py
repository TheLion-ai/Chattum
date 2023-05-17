"""Database module for the bots app."""
import os

from pydantic_models.bots import Bot
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient

mongo_client = MongoClient(os.environ["MONGODB_URL"])
database = mongo_client["bots"]


class BotsRepository(AbstractRepository[Bot]):
    """Repository for bots."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "bots"


bots_repository = BotsRepository(database=database)
