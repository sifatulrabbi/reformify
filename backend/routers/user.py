from fastapi import APIRouter
from database import DBSessionDep

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


@user_router.get("/{user_id}")
async def get_user(user_id: str, db_session: DBSessionDep):
    return 404
