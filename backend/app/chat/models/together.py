"""OpenAI models."""

from langchain_together import ChatTogether

from .base_model import LLMTemplate, UserVariable


class TogetherAIModel(LLMTemplate):
    """LLM created by OpenAI."""

    name: str = "TogetherAI"
    user_description = "Chat models from TogetherAI"
    model_type: str = "chat"
    supports_tools: bool = True

    user_variables: list[UserVariable] = [
        UserVariable(
            name="model",
            description="name of the model",
            form_type="dropdown",
            default_value="gpt-3.5-turbo",
            available_values=[
                "zero-one-ai/Yi-34B-Chat",
                "allenai/OLMo-7B-Instruct",
                "allenai/OLMo-7B-Twin-2T",
                "allenai/OLMo-7B",
                "Austism/chronos-hermes-13b",
                "cognitivecomputations/dolphin-2.5-mixtral-8x7b",
                "databricks/dbrx-instruct",
                "deepseek-ai/deepseek-coder-33b-instruct",
                "deepseek-ai/deepseek-llm-67b-chat",
                "garage-bAInd/Platypus2-70B-instruct",
                "google/gemma-2b-it",
                "google/gemma-7b-it",
                "Gryphe/MythoMax-L2-13b",
                "lmsys/vicuna-13b-v1.5",
                "lmsys/vicuna-7b-v1.5",
                "codellama/CodeLlama-13b-Instruct-hf",
                "codellama/CodeLlama-34b-Instruct-hf",
                "codellama/CodeLlama-70b-Instruct-hf",
                "codellama/CodeLlama-7b-Instruct-hf",
                "meta-llama/Llama-2-70b-chat-hf",
                "meta-llama/Llama-2-13b-chat-hf",
                "meta-llama/Llama-2-7b-chat-hf",
                "meta-llama/Llama-3-8b-chat-hf",
                "meta-llama/Llama-3-70b-chat-hf",
                "mistralai/Mistral-7B-Instruct-v0.1",
                "mistralai/Mistral-7B-Instruct-v0.2",
                "mistralai/Mixtral-8x7B-Instruct-v0.1",
                "mistralai/Mixtral-8x22B-Instruct-v0.1",
                "NousResearch/Nous-Capybara-7B-V1p9",
                "NousResearch/Nous-Hermes-2-Mistral-7B-DPO",
                "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
                "NousResearch/Nous-Hermes-llama-2-7b",
                "NousResearch/Nous-Hermes-Llama2-13b",
                "NousResearch/Nous-Hermes-2-Yi-34B",
                "openchat/openchat-3.5-1210",
                "Open-Orca/Mistral-7B-OpenOrca",
                "Qwen/Qwen1.5-0.5B-Chat",
                "Qwen/Qwen1.5-1.8B-Chat",
                "Qwen/Qwen1.5-4B-Chat",
                "Qwen/Qwen1.5-7B-Chat",
                "Qwen/Qwen1.5-14B-Chat",
                "Qwen/Qwen1.5-32B-Chat",
                "Qwen/Qwen1.5-72B-Chat",
                "Qwen/Qwen1.5-110B-Chat",
                "snorkelai/Snorkel-Mistral-PairRM-DPO",
                "Snowflake/snowflake-arctic-instruct",
                "togethercomputer/alpaca-7b",
                "teknium/OpenHermes-2-Mistral-7B",
                "teknium/OpenHermes-2p5-Mistral-7B",
                "togethercomputer/Llama-2-7B-32K-Instruct",
                "togethercomputer/RedPajama-INCITE-Chat-3B-v1",
                "togethercomputer/RedPajama-INCITE-7B-Chat",
                "togethercomputer/StripedHyena-Nous-7B",
                "Undi95/ReMM-SLERP-L2-13B",
                "Undi95/Toppy-M-7B",
                "WizardLM/WizardLM-13B-V1.2",
                "upstage/SOLAR-10.7B-Instruct-v1.0",
            ],
        ),
        UserVariable(
            name="together_api_key",
            description="your Together AI API key",
            form_type="secret",
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

    def as_llm(self) -> ChatTogether:
        """Return the LLM."""
        return ChatTogether(**self.variables_dict)
