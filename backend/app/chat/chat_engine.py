"""Chat engine."""
from abc import ABC, abstractmethod
from typing import Any, List

from langchain import ConversationChain, LLMChain
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import (
    PyPDFLoader,
    SeleniumURLLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
)
from langchain.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.prompts import BasePromptTemplate
from langchain.prompts.chat import PromptTemplate
from langchain.schema import (
    Document,
    HumanMessage,
    SystemMessage,
    messages_from_dict,
    messages_to_dict,
)
from langchain.tools import BaseTool, StructuredTool, Tool, tool
from langchain.vectorstores import Chroma

# def load_document(filename: str) -> List[Document]:
#     """Load given local file as a LangChain Document."""
#     loaders = {
#         "pdf": PyPDFLoader,
#         "txt": UnstructuredFileLoader,
#         "xls": UnstructuredExcelLoader,
#     }
#
#     extension = filename.split(".")[-1]
#     loader = loaders[extension](filename)
#     data = loader.load()
#     return data


# class SearchDocumentsTool:
#     def __init__(self, documents: List[Document]):
#         embedding_function = SentenceTransformerEmbeddings(
#             model_name="distiluse-base-multilingual-cased-v1"
#         )
#         self.db = Chroma.from_documents(documents, embedding_function)
#
#     def _run(self, query: str):
#         _docs = self.db.similarity_search(query)
#         answer = _docs[0]
#         return answer
#
#     def _arun(self, query: str):
#         raise NotImplementedError("This tool does not support async")
#
#     def as_tool(self):
#         return Tool.from_function(
#             func=self._run,
#             name="Search Documents Tool",
#             description="You must use this tool each time",
#         )


class BaseChatEngine(ABC):
    """Base class for chat engines."""

    def __init__(
        self,
        bot_id: str,
        username: str,
        user_prompt: str,
        messages: list[dict] = [],
        llm_kwargs: dict = {},
    ) -> None:
        """Initialize the chat engine."""
        self.llm: BaseLLM = self._create_llm(**llm_kwargs)
        self.prompt: BasePromptTemplate = self._create_prompt(user_prompt)
        self.memory: BaseChatMemory = self._load_memory(messages)
        self.chain: LLMChain = self._create_chain(
            bot_id, username, self.llm, self.prompt, self.memory
        )

    @abstractmethod
    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        """Load the memory from a list of messages."""
        raise NotImplementedError

    @abstractmethod
    def _create_chain(
        self,
        bot_id: str,
        username: str,
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
    ) -> ConversationChain:
        """Create a conversation chain."""
        raise NotImplementedError

    @abstractmethod
    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        """Create a prompt."""
        raise NotImplementedError

    @abstractmethod
    def _create_llm(self) -> BaseLLM:
        """Create a language model."""
        raise NotImplementedError

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.memory.chat_memory.messages)

    def chat(self, message: str) -> str:
        """Chat with the bot."""
        return self.chain.run(message)


class ChatGPTEngine(BaseChatEngine):
    """Chat engine based on GPT with prompt in the template."""

    def _create_llm(self) -> BaseLLM:
        return ChatOpenAI(temperature=0)

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            chat_memory=ChatMessageHistory(
                messages=messages_from_dict(messages), llm=self.llm
            )
        )

    def _create_chain(
        self,
        bot_id: str,
        username: str,
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
    ) -> ConversationChain:
        return ConversationChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        prompt = PromptTemplate(
            template="Human: {user_prompt}\n{history}\nHuman: {input}\nAI:",
            input_variables=["history", "input"],
            partial_variables={"user_prompt": user_prompt},
        )
        return prompt


class ChatGPTEngine2(BaseChatEngine):
    """Chat engine based on GPT with prompt as a system message."""

    def _create_llm(self) -> BaseLLM:
        return ChatOpenAI(temperature=0, verbose=True)

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        if messages == []:
            self.messages = [self.prompt]
        else:
            self.messages = messages_from_dict(messages)

    def _create_chain(
        self,
        bot_id: str,
        username: str,
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
    ) -> Any:
        class Chain:
            def __init__(self, llm: BaseLLM, messages: list[dict]):
                self.llm = llm
                self.messages = messages

            def run(self, message: str) -> str:
                message = bot_id + " " + username
                self.messages.append(HumanMessage(content=message))

                response = self.llm(self.messages)
                self.messages.append(response)
                self.memory = ConversationBufferMemory(
                    chat_memory=ChatMessageHistory(messages=self.messages, llm=self.llm)
                )
                return response.content

        return Chain(llm, self.messages)

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        prompt = SystemMessage(content=user_prompt)
        return prompt

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.chain.memory.chat_memory.messages)
