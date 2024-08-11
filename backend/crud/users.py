from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from database.user import UserModel


async def get_user_by_id(db_session: AsyncSession, user_id: str) -> UserModel:
    user = await db_session.scalar(
        select(UserModel)
        .options(joinedload(UserModel.sections))
        .where(UserModel.id == user_id)
    )
    return user


async def get_user_by_email(db_session: AsyncSession, email: str) -> UserModel:
    user = await db_session.scalar(
        select(UserModel)
        .options(joinedload(UserModel.sections))
        .where(UserModel.email == email)
    )
    return user


async def create_user(db_session: AsyncSession, data: dict[str, str]) -> UserModel:
    email = data.get("email")
    password = data.get("password")
    fullname = data.get("fullname")
    if not email or not password or not fullname:
        raise Exception(
            "Unable to create user. 'email', 'password', and 'fullname' is required."
        )

    user = UserModel(email=email, password=password, fullname=fullname)
    db_session.add(user)
    await db_session.commit()

    return user
