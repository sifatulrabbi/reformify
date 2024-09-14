from abc import ABC, abstractproperty
from langchain.prompts.chat import ChatPromptTemplate
from typing import Dict, Any


class XAgentPrompt(ABC):
    @abstractproperty
    def initial_steps(self) -> Dict[str, Any]:
        """Initial steps to prepare the Langchain agent with the necessary chat_history and tools.

        Returns:
            Dict[str, Any]: The initial steps dict.
        """
        pass

    @abstractproperty
    def chat_prompt(self) -> ChatPromptTemplate:
        """A langchain prompt that will be used with the custom langchain agent.

        Returns:
            ChatPromptTemplate: The prompt object.
        """
        pass
