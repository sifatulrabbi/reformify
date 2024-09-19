import socketio
import logging
from contextlib import asynccontextmanager
from typing import Any
from fastapi import FastAPI
from socketio.async_aiopika_manager import asyncio
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
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins=["*"],
    always_connect=False,
    transports=["websocket", "polling"],
    logger=True,
)

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


@sio.event
async def connect(sid: str, environ: dict[str, Any], auth: Any):
    print(auth, environ.keys())
    authtoken = environ.get("HTTP_AUTHORIZATION", None)
    if not authtoken:
        return False
    await sio.save_session(sid, {"username": None})
    await sio.emit(
        "message",
        {"message": f"Client '{sid}' connected.", "sid": sid},
        to=sid,
    )
    return True


@sio.event
async def disconnect(sid: str):
    logging.info(f"Client disconnected: {sid}")
    await sio.save_session(sid, None)


@sio.event
async def message(sid: str, data: dict[str, str]):
    usersession = sio.get_session(sid)
    if not usersession:
        await sio.disconnect(sid)
        return
    # handle request
    logging.info(f"handling message from: {sid}")
    print(data, end="\n\n")


@sio.event
async def test_message(sid: str, data: str):
    await asyncio.sleep(2)
    await sio.emit("test_message", data, sid)


@app.get("/health")
async def get_status():
    return {"status": "Server is running"}
