from typing import Dict
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from database import User, InjectDB

user_router = APIRouter(prefix="/users")


@user_router.get("/{user_id}")
async def get_user(user_id: str, db_session: InjectDB): ...
