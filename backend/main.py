from fastapi import FastAPI
from routers import auth_router
from db.db import migration

app = FastAPI(debug=True)
app.include_router(auth_router)
