"""Pydantic models for bots."""

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import AbstractRepository, ObjectIdField


class Bot(BaseModel):
    """Model for bots."""

    id: ObjectIdField = None  # id of bot
    name: str  # name of bot
    username: str  # name of the user associated with the bot
    tools: list = []  # list of tools that the bot can use
    sources: list = []  # list of sources that the bot can use
    prompt: str = ""  # prompt for the bot

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}


class BotsRequest(BaseModel):
    """Request model for the bots endpoint."""

    username: str  # name of the user associated with the bot
