"""
The core logic of X-Agent 001.
"""
import os
from langchain.agents import AgentExecutor
from langchain.chat_models import ChatOpenAI
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from typing import Dict

from .tools import XAgentTools
from .prompts import XAgentPrompt
from .memory import XAgentMemory


class MultiFunctionsXAgent:
    """This agent is for helping the users with their day to day business tasks.

    We will create a new instance of the agent every time a new user connects to the socket.io and will destroy it every time a user disconnects. This behavior is required because of the nature of our chat memory. The chat memory is semi-persistent means we don't store a lot info in the chat history to reduce the token usage.
    """

    def __init__(
        self, *, prompt: XAgentPrompt, tools: XAgentTools, memory: XAgentMemory
    ):
        """Initialize the MultiFunctionsAgent with a socket.io server instance and current user's session id. Finalize the agent by calling the `prepare_agent()` method.

        Args:
            prompt (CustomXAgentPrompt): The prompt that will be used with the agent.
            tools (XAgentTools): All the available tools list.

        Raises:
            ValueError: If any of the required args is not found.
        """
        self._prompt = prompt
        self._tools = tools
        self._chat_memory = memory
        self._llm = ChatOpenAI(
            temperature=0, model="gpt-3.5-turbo", verbose=self._should_log()
        )
        self._llm = self._llm.bind(functions=self._tools.openai_functions)
        self._agent = (
            self._prompt.initial_steps
            | self._prompt.chat_prompt
            | self._llm
            | OpenAIFunctionsAgentOutputParser()
        )
        self._executor = AgentExecutor(
            agent=self._agent,
            tools=self._tools.tools_list,
            memory=self._chat_memory.memory,
            max_iterations=10,  # Limited iteration count to prevent the agent from being stuck with a single task.
            handle_parsing_errors=True,  # This will let the bot handle some of the errors by itself.
            verbose=self._should_log(),
        )

    @property
    def executor(self) -> AgentExecutor:
        return self._executor

    async def invoke(self, user_msg: str) -> str:
        """Invoke the agent executor with default configs.
        If required we can use the `MultiFunctionsXAgent.executor.invoke()` to invoke with custom configs.

        Args:
            user_msg (str): The user's message. Required.

        Returns:
            str: Agent's reply
        """
        result: Dict[str, str] = await self._executor.ainvoke({"input": user_msg})
        return result.get("output")

    def _should_log(self):
        """Determines whether the agent should log it's steps or not, using the PY_ENV env."""
        PY_ENV = os.getenv("PY_ENV", "development")
        return PY_ENV == "development"
