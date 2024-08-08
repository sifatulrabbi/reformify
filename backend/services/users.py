from database import User, DBConn
from sqlalchemy.sql import select
from fastapi.exceptions import HTTPException


class UsersService:
    def __init__(self, db_conn: DBConn):
        self.db_conn = db_conn

    async def get_by_id(self, id: str) -> User | None:
        try:
            global user
            async with self.db_conn as db:
                q = select(User).where(User.id == id)
                result = await db.execute(q)
                user = result.scalar_one_or_none()
        except Exception as e:
            raise HTTPException(500, {"message": "internal error", "error": str(e)})
        if not user:
            raise HTTPException(404, {"message": "User not found"})
        return user

    async def get_by_email(self, email: str) -> User | None:
        try:
            global user
            async with self.db_conn as db:
                q = select(User).where(User.email == email)
                result = await db.execute(q)
                user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(404, {"message": "User not found"})
        except Exception as e:
            raise HTTPException(500, {"message": "internal error", "error": str(e)})
        return user

    async def create_new_user(self, payload: dict) -> User | None:
        fullname = payload.get("fullname")
        email = payload.get("email")
        password = payload.get("password")
        if not fullname or not email or not password:
            raise HTTPException(
                400,
                {
                    "message": "invalid payload. fullname, email, and password are required"
                },
            )
        try:
            global user
            async with self.db_conn as db:
                user = User(email=email, password=password, fullname=fullname)
                db.add(user)
        except Exception as e:
            raise HTTPException(500, str(e))
        return user
