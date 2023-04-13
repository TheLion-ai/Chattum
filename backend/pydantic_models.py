from typing import Optional

from pydantic import BaseModel, Extra
from typing_extensions import TypedDict


class HealthCheckResponse(BaseModel):
    status: str
