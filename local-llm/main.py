import asyncio
import whisper

# import httpx


"""
GET  http://localhost:8008/v1/models
POST http://localhost:8008/v1/chat/completions
POST http://localhost:8008/v1/completions
POST http://localhost:8008/v1/embeddings
"""
# get_llm_url = lambda p: f"http://localhost:8008/v1{p}"
# modelid = "gemma-2-2b"
# client = httpx.AsyncClient()
model = whisper.load_model("medium")


async def test_whisper():
    # filepath = "./tests/assets/simple-recording-01.m4a"
    filepath = "./tests/assets/Conversation-with-24-year-old-male-Virginia_afccal000226_003_00-10-17.mp3"
    result = model.transcribe(filepath, verbose=True)
    print("Whisper result:", result)
    return result.get("text") if result else None


# async def list_available_model():
#     res = await client.get(get_llm_url("/models"))
#     resdata = res.json()
#     print(resdata)
#     return resdata.get("data", None) if resdata else None


async def main():
    # await list_available_model()
    await test_whisper()


if __name__ == "__main__":
    asyncio.run(main())
