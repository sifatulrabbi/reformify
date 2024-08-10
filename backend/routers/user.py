from typing import Annotated
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from database import DBSessionDep
from crud.users import get_user_by_id
from auth import RequiredAuth

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


@user_router.get("/{user_id}")
async def get_user_details(
    user_id: str, access_token: RequiredAuth, db_session: DBSessionDep
):
    # get the entire user profile
    user = await get_user_by_id(db_session, access_token.sub)
    return {"user": user.to_dict()}
