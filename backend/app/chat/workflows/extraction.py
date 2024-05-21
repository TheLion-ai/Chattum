import numpy as np
from jinja2 import Environment
from langchain.llms.base import BaseLLM
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage


class ExtractionWorkflow:
    def __init__(
        self,
        entities: list[tuple],
        llm: BaseLLM,
        instructions: str = None,
    ):
        self.entities = entities
        self.instructions = instructions
        self.llm = llm.bind(logprobs=True)
        self.env = Environment()

        self.system_prompt = """
            # Expert Entity Extractor

            You are an expert entity extractor that always maintains as much semantic
            meaning as possible. You use inference or deduction whenever necessary to
            supply missing or omitted data. Examine the provided data, text, or
            information and generate a list of any entities or objects that match the
            requested format.
        """

        self.human_prompt_template = """
            ## Data to extract
            {{ data }}

            ## Entities to extract
            {% for label in labels %}
            - #{{ entity[0] }}: {{ entity[1] }}
            {% endfor %}
            {% if instructions -%}
            ## Additional instructions

            {{ instructions }}
            {% endif %}

            ## Response format

            You will return the answer in CSV format, with two columns seperated by the % character.
            First column is the extracted entity and second column is the category. Rows in the CSV are separated by new line character

        """
        self.ai_prompt = "Entity%Category\n"

    def _construct_message(self, text: str) -> list:
        human_prompt = self.env.from_string(self.human_prompt_template).render(
            entities=self.entities, data=text, instructions=self.instructions
        )
        return [
            SystemMessage(self.system_prompt),
            HumanMessage(human_prompt),
            AIMessage(self.ai_prompt),
        ]

    def predict(self, text: str) -> list[tuple]:
        messages = self._construct_message(text)
        response = self._predict(messages)
        return self._extract_entities(response)

    def _predict(self, messages: list) -> AIMessage:
        return self.llm.invoke(messages)

    def _extract_entities(self, response: AIMessage) -> list[tuple]:

        entities: list = []
        extracted_text: str = ""
        probs: list = []

        if (
            "content" in response.response_metadata["logprobs"]
            and response.response_metadata["logprobs"]["content"] is not None
        ):
            tokens = [
                token["token"]
                for token in response.response_metadata["logprobs"]["content"]
            ]
            logprobs = [
                token["logprob"]
                for token in response.response_metadata["logprobs"]["content"]
            ]
        else:
            tokens = response.response_metadata["logprobs"]["tokens"]
            logprobs = response.response_metadata["logprobs"]["token_logprobs"]

        for i, (token, logprob) in enumerate(
            zip(
                tokens,
                logprobs,
            )
        ):
            if token == "%":
                entity_name = extracted_text
                extracted_text = ""
            elif token == "\n" or i + 1 == len(
                response.response_metadata["logprobs"]["tokens"]
            ):
                entity_category = extracted_text
                extracted_text = ""
                entities.append((entity_name, entity_category, np.mean(probs)))
            else:
                extracted_text += token
                probs.append(np.exp(logprob))
        return entities
