from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import DBSessionDep
from crud.users import get_user_by_id, trim_user

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


@user_router.get("/{user_id}")
async def get_user_details(user_id: str, db_session: DBSessionDep):
    try:
        user = await get_user_by_id(db_session, user_id)
    except Exception as e:
        raise HTTPException(500, str(e))
    if not user:
        raise HTTPException(404, "User not found or invalid user id")
    return {"user": trim_user(user)}
