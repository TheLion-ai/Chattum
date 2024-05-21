import asyncio

import numpy as np
from jinja2 import Environment
from langchain.llms.base import BaseLLM
from langchain_community.chat_models import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from sklearn.calibration import CalibratedClassifierCV
from sklearn.metrics import (
    auc,
    classification_report,
    precision_recall_curve,
    roc_curve,
)
from sklearn.calibration import calibration_curve


class ClassificationWorkflow:
    def __init__(
        self,
        classes: list[str],
        llm: BaseLLM,
        instructions: str = None,
        calibrators: list = None,
    ):
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

    def encode_labels(self, labels: list[str]) -> list[int]:
        result = []
        for label in labels:
            try:
                result.append(self.class2idx[label])
            except KeyError:
                raise ValueError(f"Label {label} not found in workflow classes")
        return result

    def calibrate(self, x: list, y: list) -> None:
        calibrated_clf = CalibratedClassifierCV(self, method="isotonic", cv="prefit")
        calibrated_clf.fit(x, y)
        self.calibrators = calibrated_clf.calibrated_classifiers_[0].calibrators

    def predict(self, text: str) -> tuple:
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

    async def predict_async(self, text: str) -> tuple:
        try:
            response = await self._predict_async(text)
            return self._exctract_label(response)
        except Exception as e:
            print(f"Error: {e}")
            return None, 0.0

    def predict_proba(self, texts: list[str]) -> np.ndarray:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        tasks = [self._predict_async(text) for text in texts]
        results = loop.run_until_complete(asyncio.gather(*tasks))
        labels = [self._exctract_label(result) for result in results]
        return np.array([self._to_one_hot(label, prob) for label, prob in labels])

    def fit(self, X: list, y: list) -> None:
        pass

    def _to_one_hot(self, label: str, prob: float) -> np.ndarray:
        idx = self.class2idx[label]
        one_hot = np.zeros(len(self.classes))
        one_hot[idx] = prob
        return one_hot

    def _construct_message(self, text: str) -> list:
        human_prompt = self.env.from_string(self.human_prompt_template).render(
            labels=self.classes, data=text, instructions=self.instructions
        )
        return [
            SystemMessage(self.system_prompt),
            HumanMessage(human_prompt),
            AIMessage(self.ai_prompt),
        ]

    def _exctract_label(self, response: AIMessage) -> tuple:

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

        for token, logprob in zip(
            tokens,
            logprobs,
        ):
            if token in self.idx2class:
                return self.idx2class[token], np.exp(logprob)
        else:
            print("No valid label found in response")
            print(response.content)
            raise ValueError("No valid label found in response")

    def _predict(self, messages: list) -> AIMessage:
        return self.llm.invoke(messages)

    async def _predict_async(self, text: str) -> AIMessage:
        messages = self._construct_message(text)
        return await self.llm.ainvoke(messages)


def evaluate_classification(
    workflow: ClassificationWorkflow, x: list[str], y: list[str]
) -> dict:
    y_encoded = workflow.encode_labels(y)
    y_one_hot = np.zeros((len(y_encoded), len(workflow.classes)))
    for i, class_index in enumerate(y_encoded):
        y_one_hot[i, class_index] = 1

    probs = workflow.predict_proba(x)

    y_pred = np.argmax(probs, axis=1)

    metrics = classification_report(
        y_encoded, y_pred, target_names=workflow.classes, output_dict=True
    )
    for i in range(len(workflow.classes)):
        class_name = workflow.idx2class[str(i)]
        # Compute ROC curve and ROC area for each class
        fpr, tpr, _ = roc_curve(y_one_hot[:, i], probs[:, i])

        metrics[class_name]["fpr"] = list(fpr)
        metrics[class_name]["tpr"] = list(tpr)
        metrics[class_name]["roc_auc"] = auc(fpr, tpr)
        # Compute precision-recall curve
        precision, recall, thresholds = precision_recall_curve(
            y_one_hot[:, i], probs[:, i]
        )
        metrics[class_name]["precisions"] = list(precision)
        metrics[class_name]["recalls"] = list(recall)
        metrics[class_name]["p_r_thresholds"] = list(np.around(thresholds, 3))
        # # Compute calibration curve
        # prob_true, prob_pred = calibration_curve(
        #     y[:, class_index],
        #     y_pred[:, class_index],
        #     n_bins=10,
        # )
        # plt.plot(prob_pred, prob_true, label=f"Class {class_index}")

    return metrics
