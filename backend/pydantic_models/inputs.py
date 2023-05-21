"""Pydantic models for the input data."""
from pydantic import BaseModel


class PromptRequest(BaseModel):
    """Model for the prompt input."""

    prompt: str


class BotsRequest(BaseModel):
    """Request model for the bots endpoint."""

    username: str  # name of the user associated with the bot
