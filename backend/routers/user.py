from typing import Annotated, Dict
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.future import select
from database import User, DBConn

user_router = APIRouter(prefix="/users")
DB = Annotated[DBConn, Depends(DBConn)]


async def injectable(*args):
    print(*args)
    return True


@user_router.get("/{user_id}")
async def get_user(user_id: str, db: DB):
    user = None
    q = select(User).where(User.id == user_id)

    async with db:
        try:
            result = await db.session.execute(q)
            user = result.scalar_one_or_none()
        except Exception as e:
            await db.session.rollback()
            return JSONResponse(status_code=500, content={"message": "Internal error"})

    if user is None:
        return JSONResponse(status_code=404, content={"message": "User not found"})
    return JSONResponse(
        status_code=200,
        content={
            "data": user,
            "message": "User found",
        },
    )


@user_router.patch("/{user_id}")
async def update_user(user_id: str, data: Dict, db: DB):
    user = None
    q = select(User).where(User.id == user_id)

    async with db:
        result = await db.session.execute(q)
        user = result.scalar_one_or_none()
        if user is not None:
            for k, v in data.items():
                setattr(user, k, v)

    if user is None:
        return JSONResponse(
            status_code=404, content={"message": "No user found with the id"}
        )
    return JSONResponse(
        status_code=200,
        content={
            "message": "User updated",
            "user": user,
        },
    )


@user_router.post("/{user_id}/profile-section")
async def create_new_profile_section(user_id: str, data: Dict, db: DB):
    async with db:
        ...
    return JSONResponse(status_code=201, content={})


@user_router.patch("/{user_id}/profile-section/{section_id}")
async def update_profile_section(user_id: str, section_id: str, data: Dict, db: DB):
    async with db:
        ...
    return JSONResponse(status_code=200, content={})


@user_router.delete("/{user_id}/profile-section/{section_id}")
async def delete_profile_section(user_id: str, section_id: str, db: DB):
    async with db:
        ...
    return JSONResponse(status_code=200, content={})
