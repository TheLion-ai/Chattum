"""Gather all LLMs in one place."""
from .openai import OpenAIModel

available_models = [OpenAIModel]
available_models_dict = {model.name: model for model in available_models}
