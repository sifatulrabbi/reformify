from fastapi.exceptions import HTTPException
from sqlalchemy.sql import select
from database import DBConn, User


class UsersService:
    def __init__(self, db: DBConn):
        self._db = db

    async def get_by_id(self, id: str) -> User | None:
        try:
            async with self._db:
                q = select(User).where(User.id == id)
                result = await self._db.session.execute(q)
                user = result.scalar_one_or_none()
                return user
        except Exception as e:
            print("Error in UsersService.get_by_id()\n", e)
            return None

    async def get_by_email(self, email: str) -> User | None:
        try:
            async with self._db:
                q = select(User).where(User.email == email)
                result = await self._db.session.execute(q)
                user = result.scalar_one_or_none()
                return user
        except Exception as e:
            print("Error in UsersService.get_by_id()\n", e)
            return None

    async def create_new_user(self, payload: dict) -> User | None:
        fullname = payload.get("fullname")
        email = payload.get("email")
        password = payload.get("password")
        if not fullname or not email or not password:
            raise HTTPException(400, {"message": "invalid payload. fullname, email, and password are required"})
