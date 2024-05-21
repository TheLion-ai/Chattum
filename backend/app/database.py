"""Database module for the bots app."""
import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional

from pydantic_models.bots import Bot
from pydantic_models.conversations import Conversation
from pydantic_models.models import LLM
from pydantic_models.sources import Source
from pydantic_models.tools import Tool
from pydantic_models.workflows import Workflow
from pydantic_mongo import AbstractRepository
from pymongo import MongoClient


class BotsRepository(AbstractRepository[Bot]):
    """Repository for bots."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "bots"


class WorkflowsRepository(AbstractRepository[Workflow]):
    """Repository for workflows."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "workflows"


class ToolsRepository(AbstractRepository[Tool]):
    """Repository for tools."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "tools"


class SourcesRepository(AbstractRepository[Source]):
    """Repository for sources."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "sources"


class ConversationsRepository(AbstractRepository[Conversation]):
    """Repository for conversations."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "conversations"


class ModelsRepository(AbstractRepository[LLM]):
    """Repository for models."""

    class Meta:
        """Meta class for the repository."""

        collection_name = "models"


@dataclass
class Database:
    """Database class."""

    bots: Optional[BotsRepository] = None
    workflows: Optional[WorkflowsRepository] = None
    sources: Optional[SourcesRepository] = None
    conversations: Optional[ConversationsRepository] = None
    tools: Optional[ToolsRepository] = None
    models: Optional[ModelsRepository] = None

    def init_repositories(self, mongo_client: MongoClient) -> None:
        """Create a database repositories from a mongo client."""
        self.bots = BotsRepository(mongo_client["bots"])
        self.workflows = WorkflowsRepository(mongo_client["bots"])
        self.sources = SourcesRepository(mongo_client["bots"])
        self.conversations = ConversationsRepository(mongo_client["bots"])
        self.tools = ToolsRepository(mongo_client["bots"])
        self.models = ModelsRepository(mongo_client["bots"])


@lru_cache()
def get_mongo_client() -> MongoClient:
    """Get the database."""
    return MongoClient(os.environ["MONGODB_URL"])
