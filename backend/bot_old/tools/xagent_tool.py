from abc import ABC, abstractproperty, abstractmethod
from typing import Any, Coroutine


class XAgentTool(ABC):
    @abstractproperty
    def name(self) -> str:
        pass

    @abstractproperty
    def description(self) -> str:
        pass

    @abstractmethod
    async def tool_func(self, *args) -> Coroutine[Any, Any, Any]:
        pass
