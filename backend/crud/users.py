import logging
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from asyncpg.exceptions import UniqueViolationError
from sqlalchemy.ext.asyncio import AsyncSession
from database.user import BaseUser, BaseUserPrivate, User


async def get_user_by_id(
    db_session: AsyncSession, user_id: str
) -> BaseUserPrivate | None:
    user = await db_session.scalar(select(User).where(User.id == user_id))
    return None if user is None else serialize_user(user)


async def get_user_by_email(
    db_session: AsyncSession, email: str
) -> BaseUserPrivate | None:
    user = await db_session.scalar(select(User).where(User.email == email))
    return None if user is None else serialize_user(user)


async def create_user(
    db_session: AsyncSession, data: dict[str, str]
) -> BaseUserPrivate:
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

    return serialize_user(user)


def serialize_user(user: User) -> BaseUserPrivate:
    base_user = BaseUserPrivate(
        id=user.id,
        email=user.email,
        password=user.password,
        fullname=user.fullname,
        deleted=user.deleted,
    )
    return base_user


def trim_user(user: BaseUserPrivate) -> BaseUser:
    return BaseUser(email=user.email, id=user.id, fullname=user.fullname)
