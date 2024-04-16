"""Tools for sending requests to a url."""

import json

import requests
from pybars import Compiler
from pydantic import BaseModel, create_model

from .base_tool import ToolTemplate, UserVariable


class PostTool(ToolTemplate):
    """Tool for sending post request to a url."""

    name: str = "Post Tool"
    description: str = "use this tool to sent data to a server."

    name_for_bot: str = "post"
    description_for_bot: str = "use this tool to sent data to a server."

    user_variables: list[UserVariable] = [
        UserVariable(
            name="url", description="The url of the request", form_type="text"
        ),
        UserVariable(
            name="body", description="The body of the request", form_type="editor"
        ),
    ]

    @property
    def args_schema(self) -> BaseModel:
        """Return the args schema for langchain."""
        return create_model(
            "ArgsSchema",
            **json.loads(self.compiler.whitespace_control(self.variables_dict["body"])),
        )

    def __init__(
        self,
        user_variables: list[dict] = [],
        description_for_bot: str = None,
        name_for_bot: str = None,
    ) -> None:
        """Initialize the tool."""
        super().__init__(user_variables, description_for_bot, name_for_bot)
        self.compiler = Compiler()
        self.bot_description = description_for_bot or self.description_for_bot
        self.body_template = self.compiler.compile(self.variables_dict["body"])

    def run(self, **kwargs: dict) -> str:
        """Run the tool by sending a post request to the url with the body."""
        json_body = json.loads(self.body_template(kwargs))
        response = requests.post(json=json_body, url=self.variables_dict["url"])
        return response.text


class GetTool(ToolTemplate):
    """Tool for getting data from a url."""

    name: str = "Get Tool"
    description: str = "use this tool to get data to a server."

    name_for_bot: str = "get"
    description_for_bot: str = "use this tool to get data to a server."

    user_variables: list[UserVariable] = [
        UserVariable(
            name="url", description="The url of the request", form_type="text"
        ),
        UserVariable(
            name="body", description="The body of the request", form_type="editor"
        ),
    ]

    @property
    def args_schema(self) -> BaseModel:
        """Return the args schema for langchain."""
        return create_model(
            "ArgsSchema",
            **json.loads(self.compiler.whitespace_control(self.variables_dict["body"])),
        )

    def __init__(
        self,
        user_variables: list[dict] = [],
        description_for_bot: str = None,
        name_for_bot: str = None,
    ) -> None:
        """Initialize the tool."""
        super().__init__(user_variables, description_for_bot, name_for_bot)
        self.compiler = Compiler()
        self.body_template = self.compiler.compile(self.variables_dict["body"])

    def run(self, **kwargs: dict) -> str:
        """Run the tool by sending a post request to the url with the body."""
        json_body = json.loads(self.body_template(kwargs))
        response = requests.post(json=json_body, url=self.variables_dict["url"])
        return response.text
