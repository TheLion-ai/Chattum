import requests
from pydantic import create_model
from pybars import Compiler
import json

from .base_tool import ToolTemplate, UserVariable


class PostTool(ToolTemplate):
    name: str = "Post Tool"
    description: str = "use this tool to sent data to a server."
    user_description: str = "use this tool to sent data to a server."

    user_variables: list[UserVariable] = [
        UserVariable(name="url", description="The url of the request", form_type="text"),
        UserVariable(name="body", description="The body of the request", form_type="editor"),
    ]

    @property
    def args_schema(self):
        return create_model(
            "ArgsSchema",
            **json.loads(self.compiler.whitespace_control(self.variables_dict["body"])),
        )

    def __init__(self, user_variables: list[dict] = ...):
        super().__init__(user_variables)
        self.compiler = Compiler()
        self.body_template = self.compiler.compile(self.variables_dict["body"])

    def run(self, **kwargs):
        print(f"Received kwargs: {kwargs}")
        json_body = json.loads(self.body_template(kwargs))
        # json_body = self.body_template(name=name, age=age, color=color)
        return requests.post(json=json_body, url=self.variables_dict["url"])



    