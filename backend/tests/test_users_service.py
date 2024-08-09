if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import asyncio
from database import sessionmanager
from crud.users import create_user, get_user_by_email, get_user_by_id


mock_user = {
    "email": "test.user3@gmail.com",
    "password": "test.user3@gmail.com",
    "fullname": "test user 3",
}


async def run_tests():
    async with sessionmanager.session() as session:
        created_user = await create_user(session, mock_user)
        user_by_email = await get_user_by_email(session, mock_user["email"])
        user_by_id = await get_user_by_id(session, created_user.id)

        assert created_user is not None
        assert user_by_email is not None
        assert user_by_id is not None
        assert created_user.id == user_by_email.id and user_by_email.id == user_by_id.id


if __name__ == "__main__":
    asyncio.run(run_tests())
