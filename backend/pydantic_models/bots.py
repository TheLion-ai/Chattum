"""Pydantic models for bots."""

from bson import ObjectId
from pydantic import BaseModel
from pydantic_models.models import LLM
from pydantic_mongo import ObjectIdField


class Bot(BaseModel):
    """Model for bots."""

    id: ObjectIdField = None  # id of bot
    name: str  # name of bot
    username: str  # name of the user associated with the bot
    tools: list = []
    sources: list = []  # list of sources that the bot can use
    prompt: str = ""  # prompt for the bot
    model: LLM = None  # model for the bot

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
