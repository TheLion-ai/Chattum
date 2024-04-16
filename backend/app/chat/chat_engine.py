"""Chat engine."""

import json
from abc import ABC, abstractmethod
from typing import Any, List

from app.chat.prompts.templates import react_json
from app.chat.prompts.templates.react import conversation_with_tools
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain.agents.format_scratchpad import format_log_to_str
from langchain.agents.output_parsers import (
    JSONAgentOutputParser,
    ReActSingleInputOutputParser,
)
from langchain.agents.output_parsers.tools import ToolAgentAction
from langchain.chains import ConversationChain, LLMChain
from langchain.llms.base import BaseLLM
from langchain.memory import ConversationBufferMemory
from langchain.memory.chat_memory import BaseChatMemory
from langchain.memory.chat_message_histories.in_memory import ChatMessageHistory
from langchain.schema import SystemMessage, messages_from_dict, messages_to_dict
from langchain.tools.render import render_text_description
from langchain_community.chat_models import ChatOpenAI
from langchain_community.llms import OpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.prompts import (
    BasePromptTemplate,
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)


class NewLangChainEngine:
    def __init__(
        self,
        user_prompt: str,
        llm: BaseLLM,
        messages: list[dict] = [],
        tools: list = [],
    ) -> None:
        self.llm = llm
        self.prompt = self._create_prompt(user_prompt)
        self.messages = self._load_memory(messages)
        agent = create_openai_tools_agent(self.llm, tools, self.prompt)

        self.agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, return_intermediate_steps=True
        )

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        return ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    user_prompt,
                ),
                MessagesPlaceholder(variable_name="messages"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        return messages_from_dict(messages)

    def _get_tool_calls(self, response: dict) -> list[dict]:
        tool_calls = []

        for intermediate_step in response["intermediate_steps"]:
            print(type(intermediate_step[0]))
            if type(intermediate_step[0]) == ToolAgentAction:
                tool_calls.append(
                    {
                        "name": intermediate_step[0].tool,
                        "args": intermediate_step[0].tool_input,
                        "id": intermediate_step[0].tool_call_id,
                    }
                )
        return tool_calls

    def chat(self, message: str) -> str:
        self.messages.append(HumanMessage(content=message))
        response = self.agent_executor.invoke({"messages": self.messages})
        tool_calls = self._get_tool_calls(response)
        self.messages.append(
            AIMessage(content=response["output"], tool_calls=tool_calls)
        )
        return response["output"]

    def export_messages(self) -> list[dict]:
        return messages_to_dict(self.messages)


class BaseChatEngine(ABC):
    """Base class for chat engines."""

    def __init__(
        self,
        user_prompt: str,
        llm: BaseLLM,
        messages: list[dict] = [],
    ) -> None:
        """Initialize the chat engine."""
        self.llm: BaseLLM = llm
        self.prompt: BasePromptTemplate = self._create_prompt(user_prompt)
        self.memory: BaseChatMemory = self._load_memory(messages)
        self.chain: LLMChain = self._create_chain(
            self.llm,
            self.prompt,
            self.memory,
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
    ) -> ConversationChain:
        """Create a conversation chain."""
        raise NotImplementedError

    @abstractmethod
    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        """Create a prompt."""
        raise NotImplementedError

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.memory.chat_memory.messages)

    def chat(self, message: str) -> str:
        """Chat with the bot."""
        return self.chain.run(message)


class GPTEngine(BaseChatEngine):
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
    ) -> ConversationChain:
        return ConversationChain(llm=llm, prompt=prompt, memory=memory, verbose=True)

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        prompt = PromptTemplate(
            template="Human: {user_prompt}\n{history}\nHuman: {input}\nAI:",
            input_variables=["history", "input"],
            partial_variables={"user_prompt": user_prompt},
        )
        return prompt


class ChatGPTEngine(BaseChatEngine):
    """Chat engine based on GPT with prompt as a system message."""

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        if messages == []:
            self.messages = [self.prompt]
        else:
            self.messages = messages_from_dict(messages)

    def _create_chain(
        self, llm: BaseLLM, prompt: BasePromptTemplate, memory: BaseChatMemory
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

        return Chain(llm, self.messages)

    def _create_prompt(self, user_prompt: str) -> BasePromptTemplate:
        prompt = SystemMessage(content=user_prompt)
        return prompt

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.chain.memory.chat_memory.messages)


class BaseAgentEngine(ABC):
    """Base class for agent based chat engines."""

    def __init__(
        self,
        user_prompt: str,
        messages: list,
        tools: list,
        llm: BaseLLM,
        **kwargs: dict,
    ) -> None:
        """Initialize the chat engine."""
        self.llm: BaseLLM = llm
        self.prompt: BasePromptTemplate = self._create_prompt(user_prompt, **kwargs)
        self.memory: BaseChatMemory = self._load_memory(messages, **kwargs)
        self.agent_executor: AgentExecutor = self._create_agent(
            prompt=self.prompt, memory=self.memory, tools=tools, llm=self.llm, **kwargs
        )

    @abstractmethod
    def _create_agent(
        self,
        prompt: str,
        memory: BaseChatMemory,
        tools: list,
        llm: BaseLLM,
        **kwargs: dict,
    ) -> AgentExecutor:
        """Create an agent."""
        raise NotImplementedError

    @abstractmethod
    def _create_prompt(self, user_prompt: str, **kwargs: dict) -> BasePromptTemplate:
        """Create a prompt."""
        raise NotImplementedError

    @abstractmethod
    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        """Load the memory from a list of messages."""
        raise NotImplementedError

    def export_messages(self) -> list[dict]:
        """Export messages from the memory."""
        return messages_to_dict(self.memory.chat_memory.messages)

    def chat(self, message: str) -> str:
        """Chat with the bot."""
        return self.agent_executor.invoke({"input": message})["output"]


class ReactEngine(BaseAgentEngine):
    """Chat engine based on Re:Act with prompt in the template."""

    def _create_prompt(self, user_prompt: str, **kwargs: dict) -> BasePromptTemplate:
        return PromptTemplate.from_template(conversation_with_tools).partial(
            user_prompt=user_prompt
        )

    def _create_llm(self, **kwargs: dict) -> BaseLLM:
        return OpenAI(temperature=0, verbose=True)

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            chat_memory=ChatMessageHistory(
                messages=messages_from_dict(messages), llm=self.llm
            ),
            memory_key="chat_history",
        )

    def _create_agent(
        self,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
        tools: list,
        llm: BaseLLM,
        **kwargs: dict,
    ) -> ConversationChain:
        llm_with_stop = llm.bind(stop=["\nObservation"])
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
                "tool_names": lambda x: ", ".join([tool.name for tool in tools]),
                "tools": lambda x: "\n".join(
                    f"{tool.name}: {tool.description}" for tool in tools
                ),
            }
            | prompt
            | llm_with_stop
            | ReActSingleInputOutputParser()
        )
        return AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)


class ReactJsonEngine(BaseAgentEngine):
    """Chat engine based on Re:Act with prompt in the template."""

    def _create_prompt(self, user_prompt: str, **kwargs: dict) -> BasePromptTemplate:
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(react_json.system_prompt),
                HumanMessagePromptTemplate.from_template(react_json.user_prompt),
            ]
        )
        prompt = prompt.partial(user_prompt=user_prompt)
        return prompt

    def _load_memory(self, messages: list[dict]) -> ConversationBufferMemory:
        return ConversationBufferMemory(
            chat_memory=ChatMessageHistory(
                messages=messages_from_dict(messages), llm=self.llm
            ),
            memory_key="chat_history",
        )

    def _create_agent(
        self,
        prompt: BasePromptTemplate,
        memory: BaseChatMemory,
        tools: list,
        llm: BaseLLM,
        **kwargs: dict,
    ) -> ConversationChain:
        llm_with_stop = llm.bind(stop=["\nObservation"])
        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_log_to_str(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
                "tool_names": lambda x: ", ".join([tool.name for tool in tools]),
                "tools": lambda x: "\n".join(
                    f"{tool.name}: {tool.description}" for tool in tools
                ),
            }
            | prompt
            | llm_with_stop
            | JSONAgentOutputParser()
        )
        return AgentExecutor(agent=agent, tools=tools, verbose=True, memory=memory)
