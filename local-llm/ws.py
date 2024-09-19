import socketio
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
async def talk(sid: str, audiodata: bytes):
    pass
