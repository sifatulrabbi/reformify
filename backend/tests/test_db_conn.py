if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import unittest
from sqlalchemy.sql import select
from database import get_db_session, User


class TestUsersService(unittest.IsolatedAsyncioTestCase):
    async def test_list_tables(self):
        async with get_db_session() as db:
            try:
                # metadata = MetaData()
                # await db.run_sync(metadata.reflect)
                # table_names = metadata.tables.keys()
                # print("Tables:", list(table_names))

                q = select(User)
                result = await db.execute(q)
                users = result.fetchall()
                for user in users:
                    print(user)
            except Exception as e:
                self.fail(e)

    # async def test_bulk_insert(self):
    #     async with get_db_session() as db:
    #         pass
    #
    # async def test_selecting(self):
    #     async with get_db_session() as db:
    #         pass
    #
    # async def test_modifying_table_data(self):
    #     async with get_db_session() as db:
    #         pass


if __name__ == "__main__":
    unittest.main()
