from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.user import User


async def get_user_by_id(db_session: AsyncSession, user_id: str) -> User:
    user = await db_session.scalar(select(User).where(User.id == user_id))
    return user


async def get_user_by_email(db_session: AsyncSession, email: str) -> User:
    user = await db_session.scalar(select(User).where(User.email == email))
    return user


async def create_user(db_session: AsyncSession, data: dict[str, str]) -> User:
    email = data.get("email")
    password = data.get("password")
    fullname = data.get("fullname")
    if not email or not password or not fullname:
        raise Exception(
            "Unable to create user. 'email', 'password', and 'fullname' is required."
        )

    user = User(email=email, password=password, fullname=fullname)
    db_session.add(user)
    await db_session.commit()

    return user
