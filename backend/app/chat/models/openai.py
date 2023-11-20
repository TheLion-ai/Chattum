"""OpenAI models."""
from .base_model import LLMTemplate, UserVariable


class OpenAIModel(LLMTemplate):
    """LLM created by OpenAI."""

    name: str = "OpenAI LLM"
    user_description = "LLM created by OpenAI"

    user_variables: list[UserVariable] = [
        UserVariable(name="model", description="???", form_type="text"),
        UserVariable(name="stream", description="???", form_type="text"),
        UserVariable(name="n", description="???", form_type="text"),
        UserVariable(name="temperature", description="???", form_type="text"),
    ]
