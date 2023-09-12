"""Chat engine."""
from abc import ABC, abstractmethod
from typing import Any, List

from app.routers.documents import SearchDocumentsTool
from langchain import ConversationChain, LLMChain, OpenAI
from langchain.agents import (
    AgentExecutor,
    AgentType,
    Tool,
    ZeroShotAgent,
    initialize_agent,
)
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import (
    PyPDFLoader,
    SeleniumURLLoader,
    UnstructuredExcelLoader,
    UnstructuredFileLoader,
)
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


class BaseChatEngine(ABC):
    """Base class for chat engines."""

    def __init__(
        self,
        user_prompt: str,
        sources: list[Document],
        messages: list[dict] = [],
        llm_kwargs: dict = {},
    ) -> None:
        """Initialize the chat engine."""
        self.llm: BaseLLM = self._create_llm(**llm_kwargs)
        self.prompt: BasePromptTemplate = self._create_prompt(user_prompt)
        self.memory: BaseChatMemory = self._load_memory(messages)
        self.chain: LLMChain = self._create_chain(
            self.llm, self.prompt, self.memory, sources
        )

    @abstractmethod
    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        """Load the memory from a list of messages."""
        raise NotImplementedError

    @abstractmethod
    def _create_chain(
        self,
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
        sources: list[Document],
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
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
        sources: list[Document],
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
        llm: BaseLLM,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
        sources: list[Document],
    ) -> Any:
        class Chain:
            def __init__(self, llm: BaseLLM, messages: list[dict]):
                self.llm = llm
                self.messages = messages

            def run(self, message: str) -> str:
                self.messages.append(HumanMessage(content=message))

                response = self.llm(self.messages)
                self.messages.append(response)
                self.memory = ConversationBufferMemory(
                    chat_memory=ChatMessageHistory(messages=self.messages, llm=self.llm)
                )
                return response.content

        print(
            "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ prompt 1\n"
        )
        print(prompt)
        print(type(prompt))
        print(
            "\n@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ prompt 1 end\n"
        )

        tools = [SearchDocumentsTool(sources).as_tool()]

        prefix = """Have a conversation with a human, answering the following questions as best you can. You have access to the following tools:"""
        suffix = """Begin!"

        {chat_history}
        Question: {input}
        {agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "chat_history", "agent_scratchpad"],
        )

        memory = ConversationBufferMemory(memory_key="chat_history")
        llm_chain = LLMChain(llm=OpenAI(temperature=0), prompt=prompt)
        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools, verbose=True)
        agent_chain = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True, memory=memory
        )
        agent_chain.run(input="How many people live in canada?")
        print(
            "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ 2"
        )

        return agent_chain

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        prompt = SystemMessage(content=user_prompt)
        return prompt

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.chain.memory.chat_memory.messages)
