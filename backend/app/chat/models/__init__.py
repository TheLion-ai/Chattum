"""Gather all LLMs in one place."""
from .huggingface_hub import HugggingfaceHubModel
from .openai import ChatOpenAIModel

available_models = [ChatOpenAIModel, HugggingfaceHubModel]
available_models_dict = {model.name: model for model in available_models}
