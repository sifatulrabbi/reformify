import socketio
import logging
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from database import sessionmanager
from modules.users.router import user_router

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Reformify", debug=True)
sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=["*"], logger=True)

# app.include_router(auth_router, prefix="/reformify/api")
app.include_router(user_router, prefix="/reformify/api")
app.mount(
    "/",
    socketio.ASGIApp(
        sio,
        other_asgi_app=app,
        socketio_path="/reformify/api/socket.io",
    ),
)
connected_clients = {}


@sio.event
async def connect(sid: str, environ, auth):
    logging.info(f"Client connected: {sid}")
    connected_clients[sid] = {"username": None}
    await sio.emit(
        "message",
        {"message": f"Client '{sid}' connected.", "sid": sid},
        to=sid,
    )


@sio.event
async def disconnect(sid: str):
    logging.info(f"Client disconnected: {sid}")
    connected_clients.pop(sid, None)


@sio.event
async def set_username(sid: str, data: dict[str, Any]):
    username = data.get("username")
    if not username:
        await sio.emit("message", {"message": "No username provided."}, to=sid)
        return
    logging.info(f"setting username: {username}")
    connected_clients[sid]["username"] = username
    logging.info("username updated")
    # await sio.emit(
    #     "message",
    #     {"message": f"{username} has joined the chat."},
    #     skip_sid=sid,
    # )
    # await sio.emit("message", {"message": f"You are now known as '{username}'"}, to=sid)


@sio.event
async def chat_message(sid, data: dict[str, Any]):
    username = connected_clients[sid].get("username", "Anonymous")
    message = data.get("message")
    if not message:
        await sio.emit("message", {"message": "Empty message received."}, to=sid)
        return
    logging.info(f"from [{username}]: '{message}'")
    await sio.emit(
        "chat_message",
        {"from": username, "message": message},
        skip_sid=sid,
    )


# Example FastAPI endpoint
@app.get("/health")
async def get_status():
    return {"status": "Server is running"}
