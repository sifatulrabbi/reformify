from abc import ABC, abstractproperty
from langchain.memory.chat_memory import BaseChatMemory


class XAgentMemory(ABC):
    @abstractproperty
    def memory(self) -> BaseChatMemory:
        pass
