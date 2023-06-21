"""Models for validating requests and responses to the API."""

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


class SourceResponse(BaseModel):
    """Response model for the create source endpoint."""

    sources: list
