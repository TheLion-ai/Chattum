from jinja2 import Environment
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
import numpy as np
import asyncio
from sklearn.calibration import CalibratedClassifierCV


class ClassificationWorkflow:
    def __init__(self, classes, instructions=None, llm=None, calibrators=None):
        self.classes = classes
        self.instructions = instructions
        self.llm = llm.bind(logprobs=True)
        self.env = Environment()

        self.class2idx = {label: i for i, label in enumerate(classes)}
        self.idx2class = {str(i): label for i, label in enumerate(classes)}
        self.classes_ = np.array(list(self.idx2class.keys()))
        self._estimator_type = "classifier"
        self.calibrators = calibrators

        self.system_prompt = """
            # Expert Classifier

            You are an expert classifier that always maintains as much semantic meaning
            as possible when labeling text. You use inference or deduction whenever
            necessary to understand missing or omitted data. Classify the provided data,
            text, or information as one of the provided labels. For boolean labels,
            consider "truthy" or affirmative inputs to be "true".
        """

        self.human_prompt_template = """
            ## Text or data to classify
            {{ data }}

            {% if instructions -%}
            ## Additional instructions

            {{ instructions }}
            {% endif %}

            ## Labels

            You must classify the data as one of the following labels, which are numbered (starting from 0) and provide a brief description. Output the label number only.
            {% for label in labels %}
            - Label #{{ loop.index0 }}: {{ label }}
            {% endfor %}

        """
        self.ai_prompt = "The best label for the data is Label"

    def encode_labels(self, labels):
        result = []
        for label in labels:
            try:
                result.append(self.class2idx[label])
            except KeyError:
                raise ValueError(f"Label {label} not found in workflow classes")
        return result

    def calibrate(self, x, y):
        calibrated_clf = CalibratedClassifierCV(self, method="isotonic", cv="prefit")
        calibrated_clf.fit(x, y)
        self.calibrators = calibrated_clf.calibrated_classifiers_[0].calibrators

    def predict(self, text: str):
        messages = self._construct_message(text)
        response = self._predict(messages)
        result = self._exctract_label(response)
        if self.calibrators is not None:
            callibrated_prob = self.calibrators[self.class2idx[result[0]]].predict(
                result[1].reshape(1, -1)
            )
            return result[0], callibrated_prob[0]

        else:
            return result

    async def predict_async(self, text: str):
        try:
            messages = self._construct_message(text)
            response = await self._predict_async(messages)
            return self._exctract_label(response)
        except Exception as e:
            print(f"Error: {e}")
            return None, 0.0

    def predict_proba(self, texts: list[str]):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self._predict_async(text) for text in texts]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        labels = [self._exctract_label(result) for result in results]
        return np.array([self._to_one_hot(label, prob) for label, prob in labels])

    def fit(self, X, y):
        pass

    def _to_one_hot(self, label: str, prob: float):
        idx = self.class2idx[label]
        one_hot = np.zeros(len(self.classes))
        one_hot[idx] = prob
        return one_hot

    async def _predict_async(self, text: str):
        return self._predict(text)

    def _construct_message(self, text: str):
        human_prompt = self.env.from_string(self.human_prompt_template).render(
            labels=self.classes, data=text, instructions=self.instructions
        )
        return [
            SystemMessage(self.system_prompt),
            HumanMessage(human_prompt),
            AIMessage(self.ai_prompt),
        ]

    def _exctract_label(self, response):
        for token, logprob in zip(
            response.response_metadata["logprobs"]["tokens"],
            response.response_metadata["logprobs"]["token_logprobs"],
        ):
            if token in self.idx2class:
                return self.idx2class[token], np.exp(logprob)
        else:
            print("No valid label found in response")
            print(response.content)
            raise ValueError("No valid label found in response")

    def _predict(self, messages: list):
        return self.llm.invoke(messages)

    async def _predict_async(self, text: str):
        messages = self._construct_message(text)
        return await self.llm.ainvoke(messages)