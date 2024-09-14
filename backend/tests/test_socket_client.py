import asyncio
import threading
import statistics
from socketio.async_client import AsyncClient
from datetime import datetime


delays: list[int] = []
lock = threading.Lock()


async def handle_message(data: str):
    delay = datetime.now() - datetime.fromisoformat(data)
    with lock:
        delays.append(delay.seconds)


async def send_message(client: AsyncClient, ts: datetime):
    try:
        await client.emit("test_message", ts.isoformat())
        return True
    except Exception as e:
        print("Error while sending message:", e)
        return False


async def main():
    clients: list[AsyncClient] = []

    for _ in range(20):
        c = AsyncClient()
        c.on("test_message", handle_message)
        clients.append(c)

    for client in clients:
        try:
            await client.connect(
                url="http://localhost:8000",
                socketio_path="/reformify/api/socket.io",
            )
        except Exception as e:
            print("error while connecting to socket:", e)
            exit()

    taskgrp = []
    i = 50
    while i > 0:
        i -= 1
        ts = datetime.now()
        [
            taskgrp.append(asyncio.create_task(send_message(client, ts)))
            for client in clients
        ]
    await asyncio.gather(*taskgrp)

    await asyncio.sleep(5)
    for client in clients:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(main())

    print(f"messages received={len(delays)} expected={20*50}")
    print("max delay:", max(delays))
    print("min delay:", min(delays))
    print("average delay", statistics.mean(delays))
