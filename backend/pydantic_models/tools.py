from typing import Any

from bson import ObjectId
from pydantic import BaseModel
from pydantic_mongo import ObjectIdField


class UserVariable(BaseModel):
    name: str = ""
    description: str = ""
    value: Any = None
    form_type: str = None


class Tool(BaseModel):
    id: ObjectIdField = None
    name: str
    description: str
    user_description: str = ""
    user_variables: list[UserVariable] = []

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {ObjectId: str}
