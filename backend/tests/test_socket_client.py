import asyncio
import socketio


sio = socketio.AsyncClient()


@sio.event
async def connect():
    print("Connected to server")
    await sio.emit("set_username", {"username": "PythonClient"})


@sio.event
async def disconnect():
    print("Disconnected from server")


@sio.event
async def message(data):
    print("Message received:", data)


@sio.event
async def chat_message(data):
    print("Chat message:", data)


async def send_messages():
    while True:
        message = await aio_input('Enter message (type "quit" to exit): ')
        if message.lower() == "quit":
            break
        await sio.emit("chat_message", {"message": message})
    await sio.disconnect()


async def aio_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def main():
    await sio.connect("http://localhost:8000", socketio_path="/reformify/api/socket.io")
    await send_messages()
    await sio.wait()


if __name__ == "__main__":
    asyncio.run(main())
