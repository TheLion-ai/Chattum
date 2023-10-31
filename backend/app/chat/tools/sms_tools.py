import json

import requests
from langchain.utilities.twilio import TwilioAPIWrapper
from pybars import Compiler
from pydantic import BaseModel, create_model

from .base_tool import ToolTemplate, UserVariable


class TwilloTool(ToolTemplate):
    name: str = "Send sms tool"
    description: str = "use this tool to sent sms to a phone number."
    user_description: str = "sent sms to a phone number."

    user_variables: list[UserVariable] = [
        UserVariable(name="account_sid", description="Account SID", form_type="text"),
        UserVariable(name="auth_token", description="Auth Token", form_type="text"),
        UserVariable(name="from_number", description="From number", form_type="text"),
    ]

    @property
    def args_schema(self):
        class ArgsSchema(BaseModel):
            message: str
            to_number: str

        return ArgsSchema

    def __init__(self, user_variables: list[dict] = ...):
        super().__init__(user_variables)
        self.twilio = TwilioAPIWrapper(
            account_sid=self.variables_dict["account_sid"],
            auth_token=self.variables_dict["auth_token"],
            from_number=self.variables_dict["from_number"],
        )

    def run(self, **kwargs):
        self.twilio.run(kwargs["message"], kwargs["to_number"])
