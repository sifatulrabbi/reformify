from datetime import datetime
from typing import Any
from .xagent_tool import XAgentTool


class CurrentDateInfo(XAgentTool):
    """Helps the bot with getting current date and time info."""

    def __init__(self):
        pass

    @property
    def name(self) -> str:
        return "get_date_info"

    @property
    def description(self) -> str:
        return """Because you don't know the current date and time you need this tool to get the current date and time. This tool returns the ISO formatted current datetime in UTC."""

    async def tool_func(self) -> str:
        return datetime.now().isoformat()
