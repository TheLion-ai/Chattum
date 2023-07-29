"""Pydantic models for the input data."""
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class PromptRequest(BaseModel):
    """Model for the prompt input."""

    prompt: str


class BotsRequest(BaseModel):
    """Request model for the bots endpoint."""

    username: str  # name of the user associated with the bot


class SourceRequest(BaseModel):
    """Request model for the sources endpoint."""

    name: str  # name of the source
    type: str  # type of the source
    data: str = ""  # data of the source


class ChatInput(BaseModel):
    """Request model for the chat endpoint."""

    conversation_id: Optional[ObjectIdField] = ObjectId()  # conversation id

    message: str

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
