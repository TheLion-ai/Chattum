"""Pydantic models for LLMs."""
from typing import Any, Optional

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class UserVariable(BaseModel):
    """A user variable for a tool."""

    name: str = ""
    description: str = ""
    value: Any = None
    form_type: Optional[str] = None


class LLM(BaseModel):
    """A model."""

    id: ObjectIdField = None
    name: str
    user_description: str = ""
    user_variables: list[UserVariable] = []

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
