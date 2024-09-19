from langchain.memory import RedisChatMessageHistory, ConversationBufferMemory
from datetime import datetime
from typing import Optional
from configs import PY_ENV, REDIS_HOST
from icecream import ic

from .memory import XAgentMemory


class SemiPersistentChatMemory(XAgentMemory):
    def __init__(self, *, user_id: str, memory_key: str):
        """Initialize the SemiPersistentChatMemory.

        Args:
            user_id (str): The user's id (required).
            memory_key (str): The key where the chat history will load. Probably get it from `CustomXAgentPrompt`
        """
        if not user_id or not memory_key:
            raise ValueError(
                "`user_id` and `memory_key` is required to instantiate the Memory."
            )
        self._user_id = user_id
        message_history = RedisChatMessageHistory(
            url=self._get_redis_url(), ttl=600, session_id=self._user_id
        )
        self._memory = ConversationBufferMemory(
            memory_key=memory_key, chat_memory=message_history
        )
        self._inactivity_threshold = 60 * 60 * 6.0 if PY_ENV == "production" else 0.0

    @property
    def memory(self):
        return self._memory

    def _get_redis_url(self) -> str:
        """Get the redis connection url"""
        # TODO: validate and verify the redis db before sending back the url. This will prevent any complicated errors related to redis.
        port = "6379"
        return f"redis://{REDIS_HOST}:{port}"

    async def _reset_if_met_threshold(self, last_update_time: Optional[str] = None):
        """Reset the chat history after 4 hours of inactivity.

        Args:
            last_update_time (str, optional): Datetime string in ISO format.
        """
        if not last_update_time:
            return

        update_time = datetime.fromisoformat(last_update_time)
        current_time = datetime.utcnow()
        difference = current_time - update_time
        if difference.total_seconds() > self._inactivity_threshold:
            self._memory.clear()
