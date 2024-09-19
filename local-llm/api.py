import fastapi
import socketio
from ws import sio


app = fastapi.FastAPI(debug=True, title="Reformify")
app.mount(
    "/reformify/api",
    socketio.ASGIApp(sio, app, socketio_path="/reformify/api/ws"),
    "Reformify - WebSocket",
)
