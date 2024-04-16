"""Base class for all tools."""

from abc import ABC, abstractmethod
from typing import Any

from langchain.tools import StructuredTool
from pydantic import BaseModel
from pydantic_models.tools import UserVariable


class ToolTemplate(ABC):
    """Base class for all tools."""

    name: str  # name of the tool for user
    description: str  # description of the tool for user

    description_for_bot: str  # description of the tool for bot
    name_for_bot: str  # name of the tool for bot

    user_variables: list[UserVariable] = []

    def __init__(
        self,
        user_variables: list[dict] = [],
        description_for_bot: str = None,
        name_for_bot: str = None,
    ) -> None:
        """Initialize the tool using the user variables."""
        self.user_variables = user_variables
        self.description_for_bot = description_for_bot or self.description_for_bot
        self.name_for_bot = name_for_bot or self.name_for_bot
        self._create_user_variables_dict()

    def _create_user_variables_dict(self) -> None:
        """Create a dictionary of the user variables with the variable name as the key."""
        self.variables_dict = {var.name: var.value for var in self.user_variables}

    @property
    @abstractmethod
    def args_schema(self) -> BaseModel:
        """Return the args schema for langchain."""
        raise NotImplementedError

    @property
    def tool_description(self) -> str:
        """Return the tool description for llm in form tool_name(arg1:type, arg2:type) - tool_description."""
        args = self.args_schema.__fields__
        return f"{self.name_for_bot}({', '.join([a.name +':'+str(a._type_display()) for a in args.values()])}) - {self.description_for_bot}"

    @abstractmethod
    def run(self, **kwargs: dict) -> Any:
        """Run the tool with variables."""
        raise NotImplementedError

    def as_tool(self) -> StructuredTool:
        """Return the tool as a langchain StructuredTool."""
        tool = StructuredTool.from_function(
            func=self.run,
            name=self.name_for_bot,
            description=self.description_for_bot,
            args_schema=self.args_schema,
        )
        tool.description = self.tool_description
        return tool

    @classmethod
    @property
    def template(self) -> dict:
        """Return the template for the tool for the frontend."""
        return {
            "name": self.name,
            "description": self.description,
            "user_variables": self.user_variables,
            "description_for_bot": self.description_for_bot,
            "name_for_bot": self.name_for_bot,
        }
