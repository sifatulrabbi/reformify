from fastapi import FastAPI
from routers import auth_router, user_router

app = FastAPI(debug=True)
app.include_router(auth_router)
app.include_router(user_router)
