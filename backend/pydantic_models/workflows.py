"""Pydantic models for bots."""

from typing import List, Optional

from bson import Binary, ObjectId
from pydantic import BaseModel
from pydantic_models.models import LLM
from pydantic_mongo import ObjectIdField


class Workflow(BaseModel):
    """Model for workflow."""

    id: ObjectIdField = None  # id of workflow
    name: str  # name of workflow
    username: str  # name of the user associated with the workflow
    task: str = ""  # task of the workflow
    model: LLM = None  # model for the workflow
    calibrators: Optional[Binary] = None  # sklearn model
    classes: Optional[List[str]] = None
    class_thresholds: Optional[dict[str, float]] = None
    instructions: Optional[str] = None

    class Config:
        """The ObjectIdField creates an bson ObjectId value, so its necessary to setup the json encoding"."""

        json_encoders = {
            ObjectId: str,
            Binary: lambda v: "Sklearn model" if v else None,
        }


class WorkflowSettings(BaseModel):
    """Model for workflow settings."""

    instructions: str
    classes: list[str]
