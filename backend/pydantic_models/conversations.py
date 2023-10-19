"""Pydantic models for conversations."""
import datetime

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class Conversation(BaseModel):
    """Model for conversations."""

    id: ObjectIdField = None  # conversation id
    bot_id: ObjectIdField = None  # bot id
    messages: list = []  # list of messages
    last_message_time: datetime.datetime | None = None

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
