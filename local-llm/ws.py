import socketio
import aiofiles
import tempfile
from uuid import uuid4
from typing import Any

__all__ = ["sio"]

sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["*"],
    always_connect=False,
    transports=["websocket", "polling"],
    logger=True,
)


@sio.event
async def connect(sid: sid, environ: dict[str, Any], auth: Any) -> bool:
    return True


@sio.event
async def transcribe_chunk(sid: str, audiodata: bytes):
    filename = sid + "-" + str(uuid4())
    print(filename)
    async with tempfile.NamedTemporaryFile(suffix=".mp3", delete_on_close=True) as tf:
        pass
