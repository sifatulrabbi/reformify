from datetime import datetime
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from database import DBSessionDep
from modules.auth import enforce_apikey_auth
from database.user import UserCareerModel, BaseUserCareer
from sqlalchemy.sql import delete, select
from .schemas import CreateUserPayload
from .crud import create_user, get_user_by_id

__all__ = ["user_router"]


user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(enforce_apikey_auth)],
)


@user_router.post("/", description="Create a new user profile in reformify")
async def create_user_profile(payload: CreateUserPayload, db_sessoin: DBSessionDep):
    try:
        user = await create_user(db_sessoin, payload.model_dump())
        return JSONResponse(
            {"user": user.to_dict(), "message": "New reformify user profile created"},
            status_code=201,
        )
    except Exception as e:
        return JSONResponse(
            {"message": f"Unable to create user profil. Error: {str(e)}"},
            status_code=400,
        )


@user_router.get("/{user_id}")
async def get_user_details(user_id: str, db_session: DBSessionDep):
    user = await get_user_by_id(db_session, user_id)
    return {"user": user.to_dict()}


#### careers routes ####


@user_router.get("/{user_id}/careers")
async def get_all_career_entries(user_id: str, db_session: DBSessionDep):
    try:
        entries = (
            await db_session.scalars(
                select(UserCareerModel).where(UserCareerModel.user_id == user_id)
            )
        ).all()
        entries_list: list[dict] = []
        for e in entries:
            if not e:
                continue
            entries_list.append(e.to_dict())
        return {
            "careers": entries_list,
            "messgaes": "Career entries found",
        }
    except Exception as e:
        return JSONResponse(
            {"message": f"Unable to get career entries. Error: {str(e)}"},
            status_code=400,
        )


@user_router.post("/{user_id}/careers")
async def add_career_entry_to_the_profile(
    user_id: str,
    payload: BaseUserCareer,
    db_session: DBSessionDep,
):
    career = UserCareerModel(
        user_id=UUID(user_id),
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
    user = await get_user_by_id(db_session, user_id)
    return {
        "user": user,
        "career": career.serialize(),
    }


@user_router.patch("/{user_id}/careers/{career_id}")
async def update_career_entry(
    user_id: str,
    career_id: str,
    payload: dict,
    db_session: DBSessionDep,
):
    try:
        career = await db_session.scalar(
            select(UserCareerModel).where(UserCareerModel.id == career_id)
        )
        if not career or career.user_id is not user_id:
            return JSONResponse({"message": "Selected career entry not found!"}, 400)
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
        await db_session.refresh(career)
        return {"career": career.to_dict()}
    except Exception as e:
        raise HTTPException(500, str(e))


@user_router.delete("/{user_id}/careers/{career_id}")
async def delete_career_entry(user_id: str, career_id: str, db_session: DBSessionDep):
    try:
        await db_session.execute(
            delete(UserCareerModel)
            .where(UserCareerModel.user_id == user_id)
            .where(UserCareerModel.id == career_id)
        )
        return JSONResponse({"message": "Career entry deleted"})
    except Exception as e:
        return JSONResponse(
            {"message": f"Unable to delete the entry. Error: {str(e)}"},
            status_code=400,
        )
