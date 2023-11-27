"""OpenAI models."""
from langchain.chat_models import ChatOpenAI

from .base_model import LLMTemplate, UserVariable


class ChatOpenAIModel(LLMTemplate):
    """LLM created by OpenAI."""

    name: str = "ChatGPT"
    user_description = "OpenAI chat model"
    model_type: str = "chat"
    supports_tools: bool = True

    user_variables: list[UserVariable] = [
        UserVariable(
            name="model",
            description="name of the model",
            form_type="text",
            default_value="gpt-3.5-turbo",
        ),
        UserVariable(
            name="openai_api_key", description="your OpenAI API key", form_type="text"
        ),
        # UserVariable(name="stream", description="???", form_type="text"),
        # UserVariable(name="n", description="???", form_type="text"),
        UserVariable(
            name="temperature",
            description="temperature for the model",
            form_type="float",
            default_value=0.9,
        ),
    ]

    def as_llm(self) -> ChatOpenAI:
        """Return the LLM."""
        return ChatOpenAI(**self.variables_dict)
