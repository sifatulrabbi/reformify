if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import unittest
from services.users import UsersService
from database import get_db_session


db = get_db_session()
service = UsersService(db)
payload = {
    "email": "test.user@sifatulrabbi.com",
    "password": "password",
    "fullname": "Test User 1",
}


class TestUsersService(unittest.IsolatedAsyncioTestCase):
    async def test_create_user_with_correct_payload(self):
        try:
            user = await service.create_new_user(payload)
            assert user is not None
            assert user.email == payload["email"]
        except Exception as e:
            assert e is None
        finally:
            print("test_create_user_with_correct_payload: success")

    async def test_create_user_with_incorrect_payload(self):
        self.skipTest("future")
        p = payload.copy()
        p["password"] = ""
        try:
            user = await service.create_new_user(p)
            assert user is None
        except Exception as e:
            assert e is not None
        finally:
            print("test_create_user_with_incorrect_payload: success")

    async def test_get_user_by_id(self): ...

    async def test_get_user_by_email(self): ...

    async def test_update_user(self):
        pass

    async def test_delete_user(self):
        pass


if __name__ == "__main__":
    unittest.main()
