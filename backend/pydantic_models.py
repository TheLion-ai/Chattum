""" Models for validating requests and responses to the API.
"""

from pydantic import BaseModel


class HealthCheckResponse(BaseModel):
    status: str
