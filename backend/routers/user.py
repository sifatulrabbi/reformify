from uuid import UUID
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from database import DBSessionDep
from crud.users import get_user_by_id
from auth import RequiredAuth
from database.user import UserCareerModel, BaseUserCareer


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"message": "Not found"}},
)


@user_router.get("/{user_id}")
async def get_user_details(
    user_id: str, access_token: RequiredAuth, db_session: DBSessionDep
):
    if user_id != access_token.sub:
        raise HTTPException(403, "Please login to your account first.")
    user = await get_user_by_id(db_session, access_token.sub)
    return {"user": user.to_dict()}


@user_router.post("/{user_id}/careers")
async def add_career_entry_to_the_profile(
    user_id: str,
    access_token: RequiredAuth,
    payload: BaseUserCareer,
    db_session: DBSessionDep,
):
    if user_id != access_token.sub:
        raise HTTPException(403, "Please login to your account first.")

    career = UserCareerModel(
        user_id=UUID(access_token.sub),
        title=payload.title,
        company=payload.company,
        job_type=payload.job_type,
        start_date=payload.start_date,
        description=payload.description,
        company_description=payload.company_description,
        job_location=payload.job_location,
        company_location=payload.company_location,
        end_date=payload.end_date,
    )
    db_session.add(career)
    await db_session.commit()
    user = await get_user_by_id(db_session, access_token.sub)
    return {
        "user": user,
        "career": career.serialize(),
    }
