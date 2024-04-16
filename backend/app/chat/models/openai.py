"""OpenAI models."""

from langchain_community.chat_models import ChatOpenAI

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
            form_type="dropdown",
            default_value="gpt-3.5-turbo",
            available_values=[
                "gpt-4-turbo",
                "gpt-4",
                "gpt-4-32k",
                "gpt-3.5-turbo",
                "gpt-3.5-turbo-1106",
            ],
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
