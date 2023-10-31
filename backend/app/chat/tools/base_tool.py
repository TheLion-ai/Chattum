from abc import ABC, abstractmethod
from pydantic import BaseModel
from typing import Any
from langchain.tools import StructuredTool
from pydantic_models.tools import UserVariable


class ToolTemplate:
    name: str
    description: str
    user_description: str

    user_variables: list[UserVariable] = []

    def __init__(self, user_variables: list[dict] = []):
        self.set_user_variables(user_variables)
        self._create_user_variables_dict()
        

    def _create_user_variables_dict(self):
        self.variables_dict = {var.name: var.value for var in self.user_variables}

    @property
    @abstractmethod
    def args_schema(self) -> BaseModel:
        raise NotImplementedError

    @property
    def tool_description(self):
        args = self.args_schema.__fields__
        return f"{self.name}({', '.join([a.name +':'+str(a._type_display()) for a in args.values()])}) - {self.description}"

    @abstractmethod
    def run(self, **kwargs):
        raise NotImplementedError

    def as_tool(self):
        tool = StructuredTool.from_function(
            func=self.run,
            name=self.name,
            description=self.description,
            args_schema=self.args_schema,
        )
        tool.description = self.tool_description
        return tool

    @classmethod
    @property
    def template(self):
        return {
            "name": self.name,
            "description": self.description,
            "user_variables": self.user_variables,
            "user_description": self.user_description,
        }

    def set_user_variables(self, variables: list[dict]):
        self.user_variables = variables
