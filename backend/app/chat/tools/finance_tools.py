"""Tool for checking currency exchange rates"""
from langchain.utilities.alpha_vantage import AlphaVantageAPIWrapper
from pydantic import BaseModel

from .base_tool import ToolTemplate, UserVariable


class FinanceTool(ToolTemplate):
    """Tool for checking currency exchange rates"""

    name: str = "Currency exchange Tool"
    user_description: str = "Use the AlphaVantageAPIWrapper to get currency exchange rates."

    user_variables: list[UserVariable] = [
        UserVariable(name="api_key", description="AlphaVantage API key", form_type="text")
    ]

    @property
    def args_schema(self) -> BaseModel:
        class ArgsSchema(BaseModel):
            from_currency: str
            to_currency: str

        return ArgsSchema

    def __init__(self, user_variables: list[dict] = []):
        """Initialize tool"""
        super().__init__(user_variables)
        self.alpha_vantage = AlphaVantageAPIWrapper()

    def run(self, **kwargs: dict) -> str:
        """Run tool"""
        self.alpha_vantage.run(kwargs["from_currency"], kwargs["to_currency"])
        return 0

    @property
    def description(self) -> str:
        """Return the tool description for llm."""
        return "use this tool to get currency exchange rates."
