from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ConfigDict
from database import DBSessionDep
from crud.users import get_user_by_id
from auth import RequiredAuth

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


class AddCareerEntryPayload(BaseModel):
    model_config = ConfigDict(from_attributes=True)


@user_router.get("/{user_id}")
async def get_user_details(
    user_id: str, access_token: RequiredAuth, db_session: DBSessionDep
):
    # get the entire user profile
    user = await get_user_by_id(db_session, access_token.sub)
    return {"user": user.to_dict()}


@user_router.post("/{user_id}/careers")
async def add_career_entry_to_the_profile(
    access_token: RequiredAuth,
    user_id: str,
    payload: AddCareerEntryPayload,
    db_session: DBSessionDep,
):
    return {"body": payload}
