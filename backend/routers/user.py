from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import DBSessionDep
from crud.users import get_user_by_id
from auth import RequiredAuth
from database.user import BaseUser

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


@user_router.get("/{user_id}")
async def get_user_details(user_id: str, db_session: DBSessionDep, user: RequiredAuth):
    return {"user": user}
