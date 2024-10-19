import fastapi
import socketio
from fastapi.middleware.cors import CORSMiddleware
from ws import sio


app = fastapi.FastAPI(debug=True, title="Reformify")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/reformify/api",
    socketio.ASGIApp(sio, app, socketio_path="/reformify/api/ws"),
    "Reformify - WebSocket",
)
