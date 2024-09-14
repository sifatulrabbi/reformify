import asyncio
import threading
import statistics
from socketio.async_client import AsyncClient
from datetime import datetime


clients: list[AsyncClient] = []
delays: list[int] = []
connections: int = 0
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


async def main(clients_count: int, msg_per_client: int, keepalive: int = 10):
    for _ in range(clients_count):
        c = AsyncClient()
        c.on("test_message", handle_message)
        clients.append(c)

    for client in clients:
        try:
            await client.connect(
                url="http://localhost:8000",
                socketio_path="/reformify/api/socket.io",
                headers={"Authorization": "Bearer helloworld"},
            )
            with lock:
                global connections
                connections += 1
        except Exception as e:
            print("connections stablished:", connections)
            print("error while connecting to socket:", e)
            exit()
    print("connections stablished:", connections)

    taskgrp = []
    i = msg_per_client
    while i > 0:
        i -= 1
        ts = datetime.now()
        [
            taskgrp.append(asyncio.create_task(send_message(client, ts)))
            for client in clients
        ]
    await asyncio.gather(*taskgrp)

    await asyncio.sleep(keepalive)
    for client in clients:
        await client.disconnect()

    print(f"messages received={len(delays)} expected={clients_count*msg_per_client}")
    print("max delay:", max(delays))
    print("min delay:", min(delays))
    print("average delay", statistics.mean(delays))


if __name__ == "__main__":
    try:
        asyncio.run(main(1, 0, 2))
    except:
        pass
