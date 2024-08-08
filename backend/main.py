from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import auth_router, user_router
from database import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    if sessionmanager._engine is not None:
        await sessionmanager.close()


app = FastAPI(lifespan=lifespan, title="Reformify", debug=True)

app.include_router(auth_router, prefix="/reformify/api")
app.include_router(user_router, prefix="/reformify/api")
