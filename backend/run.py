import uvicorn
import asyncio
from configs import PORT
from database import migration

if __name__ == "__main__":
    asyncio.run(migration())
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=True)
