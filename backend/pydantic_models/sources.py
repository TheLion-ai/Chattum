"""Pydantic models for sources."""
from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class Source(BaseModel):
    """Model for sources."""

    id: ObjectIdField = None  # id of source
    name: str  # name of source
    type: str  # type of source

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
