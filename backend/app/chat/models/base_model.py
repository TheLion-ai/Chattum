"""Base class for all LLMs."""
from abc import ABC, abstractmethod

from pydantic_models.models import UserVariable


class LLMTemplate(ABC):
    """Base class for all LLMs."""

    name: str
    user_description: str

    user_variables: list[UserVariable] = []

    def __init__(self, user_variables: list[dict] = []):
        """Initialize LLM using user variables."""
        self.user_variables = user_variables
        self._create_user_variables_dict()

    def _create_user_variables_dict(self) -> None:
        """Create a dictionary of the user variables with the variable name as the key."""
        self.variables_dict = {var.name: var.value for var in self.user_variables}
