"""Models for validating requests and responses to the API."""

from bson import ObjectId
from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str


class MessageResponse(BaseModel):
    """Simple response with a message."""

    message: str


class CreateBotResponse(BaseModel):
    """Response model for the create bot endpoint."""

    message: str
    bot_id: str


class PromptResponse(BaseModel):
    """Response model for the create prompt endpoint."""

    prompt: str


class CreateConversationResponse(BaseModel):
    """Response model for the create conversation endpoint."""

    message: str
    conversation_id: str


class CreateSourceResponse(BaseModel):
    """Response model for the create source endpoint."""

    message: str
    source_id: str


class SourceResponse(BaseModel):
    """Response model for the create source endpoint."""

    sources: list = []

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
