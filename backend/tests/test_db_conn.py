if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import unittest
from sqlalchemy.sql import delete, insert, select
from database import get_db_session, User


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
        async with get_db_session() as db:
            try:
                dbusers = [User(**u) for u in mock_users]
                db.add_all(dbusers)
                for u in dbusers:
                    users.append(u.serialize())
                    print(u.serialize())
            except Exception as e:
                self.fail(e)

    async def test_selecting(self):
        self.skipTest("skip")
        async with get_db_session() as db:
            try:
                u = users[0]
                result = await db.execute(select(User).where(User.id == u.get("id")))
                user = result.scalar_one_or_none()
                assert user is not None
                user = user.serialize()
                assert user is not None
                assert user.get("email") == u.get("email")
            except Exception as e:
                self.fail(e)

    # async def test_modifying_table_data(self):
    #     async with get_db_session() as db:
    #         pass

    async def test_delete_entries(self):
        async with get_db_session() as db:
            await db.execute(delete(User))


if __name__ == "__main__":
    unittest.main()
