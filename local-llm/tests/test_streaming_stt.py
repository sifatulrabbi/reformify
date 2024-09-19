import asyncio


filepath = "./tests/assets/eng-us-linguistics_mp3.zip"


async def runtest():
    with open(filepath) as f:
        pass


if __name__ == "__main__":
    asyncio.run(runtest())
