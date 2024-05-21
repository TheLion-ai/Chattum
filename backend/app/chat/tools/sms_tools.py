"""Tool for sending sms to a phone number using twillio.""" ""


from typing import Optional

from langchain_community.utilities import TwilioAPIWrapper
from pybars import Compiler
from pydantic import BaseModel, create_model

from .base_tool import ToolTemplate, UserVariable


class TwilloTool(ToolTemplate):
    """Tool for sending sms to a phone number using twillio."""

    name: str = "Send SMS Tool"
    description: str = "sent sms to a phone number."

    name_for_bot: str = "send_sms"
    description_for_bot: str = "use this tool to sent data to a server."

    user_variables: list[UserVariable] = [
        UserVariable(name="account_sid", description="Account SID", form_type="text"),
        UserVariable(name="auth_token", description="Auth Token", form_type="text"),
        UserVariable(name="from_number", description="From number", form_type="text"),
    ]

    @property
    def args_schema(self) -> BaseModel:
        """Return the args schema for langchain."""

        class ArgsSchema(BaseModel):
            message: str
            to_number: str

        return ArgsSchema

    def __init__(
        self, user_variables: list[dict] = [], bot_description: Optional["str"] = None
    ) -> None:
        """Initialize the tool using the user variables with TwilioAPIWrapper."""
        super().__init__(user_variables)
        self.twilio = TwilioAPIWrapper(
            account_sid=self.variables_dict["account_sid"],
            auth_token=self.variables_dict["auth_token"],
            from_number=self.variables_dict["from_number"],
        )

    def run(self, **kwargs: dict) -> str:
        """Run the tool."""
        self.twilio.run(kwargs["message"], kwargs["to_number"])
        return "message sent"
