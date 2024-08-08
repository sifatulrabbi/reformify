if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import unittest
from sqlalchemy.sql import delete, insert, select
from database import sessionmanager
from database.user import User


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


class TestUsersService(unittest.IsolatedAsyncioTestCase):
    async def test_list_tables(self):
        self.skipTest("Not implemented yet.")

    async def test_bulk_insert(self):
        self.skipTest("already tested")
        dbusers = [User(**u) for u in mock_users]
        async with sessionmanager.session() as session:
            session.add_all(dbusers)
            await session.commit()

    async def test_selecting(self):
        # self.skipTest("skip")
        async with sessionmanager.session() as session:
            user = await session.scalar(
                select(User).where(User.email == mock_users[0]["email"])
            )
            assert user is not None
            assert user.email == mock_users[0]["email"]
            assert user.fullname == mock_users[0]["fullname"]

    async def test_delete_entries(self):
        async with sessionmanager.session() as session:
            # await session.execute(delete(User))
            # await session.commit()
            pass


if __name__ == "__main__":
    unittest.main()
