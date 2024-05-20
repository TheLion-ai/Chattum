"""Gather all LLMs in one place."""

from .huggingface_hub import HugggingfaceHubModel
from .openai import ChatOpenAIModel
from .together import TogetherAIModel

available_models = [ChatOpenAIModel, HugggingfaceHubModel, TogetherAIModel]
available_models_dict = {model.name: model for model in available_models}
