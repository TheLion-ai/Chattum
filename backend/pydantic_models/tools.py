from pydantic import BaseModel
from typing import Any
from pydantic_mongo import ObjectIdField
from bson import ObjectId

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
