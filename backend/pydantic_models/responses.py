"""Models for validating requests and responses to the API."""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    """Response model for the health check endpoint."""

    status: str


class MessageResponse(BaseModel):
    """Simple response with a message."""

    message: str
