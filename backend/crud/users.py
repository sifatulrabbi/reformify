from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.user import BaseUser, BaseUserPrivate, User


def serialize_user(user: User) -> BaseUserPrivate: ...


def deserialize_user(user: BaseUserPrivate | BaseUser) -> User: ...


def trim_user(user: BaseUserPrivate) -> BaseUser: ...


async def get_user_by_id(
    db_session: AsyncSession, user_id: str
) -> BaseUserPrivate | None:
    user = await db_session.scalar(select(User).where(User.id == user_id))
    return serialize_user(user)


async def get_user_by_email(
    db_session: AsyncSession, user_id: str
) -> BaseUserPrivate | None:
    return None
