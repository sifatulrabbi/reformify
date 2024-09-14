import asyncio
import socketio
from sqlalchemy import except_


sio = socketio.AsyncClient()


@sio.event
async def connect():
    pass


# @sio.event
# async def accepting_profile(sid: str):
#     print("-- setting username --")
#     await sio.emit("set_username", {"username": sid})


@sio.event
async def disconnect():
    print("-- Disconnected from server --")


@sio.event
async def message(data: dict[str, str]):
    print(f">> {data.get('message')}")
    # if data.get("sid", None):
    #     print("-- setting username --")
    #     try:
    #         await sio.emit(event="set_username", data={"username": data.get("sid")})
    #     except Exception as e:
    #         print("error while setting username", e)


@sio.event
async def chat_message(data):
    print(f"[{data.get('from')}]: {data.get('message')}")


async def send_messages():
    while True:
        message = await aio_input('Enter message (type "q" to exit): ')
        if message.lower() == "q":
            break
        await sio.emit("chat_message", {"message": message})


async def aio_input(prompt):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, input, prompt)


async def main():
    try:
        await sio.connect(
            "http://localhost:8000", socketio_path="/reformify/api/socket.io"
        )
        await send_messages()
        # await sio.wait()
        await sio.disconnect()
        exit()
    except:
        exit()


if __name__ == "__main__":
    asyncio.run(main())
