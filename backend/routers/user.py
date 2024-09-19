from datetime import datetime
from uuid import UUID
from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from database import DBSessionDep
from crud.users import get_user_by_id
from auth import RequiredAuth
from database.user import UserCareerModel, BaseUserCareer
from sqlalchemy.sql import select


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


@user_router.patch("/{user_id}/careers/{career_id}")
async def update_career_entry(
    user_id: str,
    career_id: str,
    access_token: RequiredAuth,
    payload: dict,
    db_session: DBSessionDep,
):
    if user_id != access_token.sub:
        raise HTTPException(403, "Please login to your account first.")

    try:
        career = await db_session.scalar(
            select(UserCareerModel).where(UserCareerModel.id == career_id)
        )
        if not career:
            return JSONResponse({"message": "Selected career entry not found!"}, 404)
    except Exception as e:
        raise HTTPException(500, str(e))

    if "title" in payload and isinstance(payload["title"], str):
        career.title = payload["title"]
    if "company" in payload and isinstance(payload["company"], str):
        career.company = payload["company"]
    if "job_type" in payload and isinstance(payload["job_type"], str):
        career.job_type = payload["job_type"]
    if "job_location" in payload and isinstance(payload["job_location"], str):
        career.job_location = payload["job_location"]
    if "company_location" in payload and isinstance(payload["company_location"], str):
        career.company_location = payload["company_location"]
    if "description" in payload and isinstance(payload["description"], list):
        career.description = payload["description"]
    if "company_description" in payload and isinstance(
        payload["company_description"], str
    ):
        career.company_description = payload["company_description"]
    if "start_date" in payload and isinstance(payload["start_date"], str):
        try:
            ts = datetime.fromisoformat(payload["start_date"])
            career.start_date = ts
        except Exception:
            pass
    if "end_date" in payload and isinstance(payload["end_date"], str):
        try:
            ts = datetime.fromisoformat(payload["end_date"])
            career.end_date = ts
        except Exception:
            pass

    try:
        await db_session.commit()
        return {"career": career.to_dict()}
    except Exception as e:
        raise HTTPException(500, str(e))
