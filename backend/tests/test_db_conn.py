if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import delete, select
from database import sessionmanager
from database.user import UserModel


mock_users = [
    {
        "email": "test.user1@gmail.com",
        "password": "test.user1@gmail.com",
        "fullname": "test user1",
    },
    {
        "email": "test.user2@gmail.com",
        "password": "test.user2@gmail.com",
        "fullname": "test user 2",
    },
    {
        "email": "test.user3@gmail.com",
        "password": "test.user3@gmail.com",
        "fullname": "test user 3",
    },
]
users = []


async def test_bulk_insert(session: AsyncSession):
    dbusers = [UserModel(**u) for u in mock_users]
    session.add_all(dbusers)
    await session.commit()


async def test_selecting(session: AsyncSession):
    user = await session.scalar(
        select(UserModel).where(UserModel.email == mock_users[0]["email"])
    )
    assert user is not None
    assert user.email == mock_users[0]["email"]
    assert user.fullname == mock_users[0]["fullname"]


async def test_delete_entries(session: AsyncSession):
    await session.execute(delete(UserModel))
    await session.commit()


async def run_tests():
    async with sessionmanager.session() as session:
        await test_bulk_insert(session)
        await test_selecting(session)
        await test_delete_entries(session)


if __name__ == "__main__":
    asyncio.run(run_tests())
