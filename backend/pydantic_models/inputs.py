"""Pydantic models for the input data."""
from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, validator
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
    source_type: str  # type of the source
    data: str = ""  # data of the source


class ChatInput(BaseModel):
    """Request model for the chat endpoint."""

    conversation_id: Optional[ObjectIdField]  # = ObjectId()  # conversation id

    message: str

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}

    @validator("conversation_id", pre=True, always=True)
    def set_conversation_id(cls, v: ObjectId | None) -> ObjectId:
        """When conversation_id is None then create a new conversation."""
        return v or ObjectId()
    

class ClassificationInput(BaseModel):
    """Request model for the classification endpoint."""

    message: str  # data to be classified
