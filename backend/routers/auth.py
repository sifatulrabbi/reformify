import jwt
from datetime import timedelta, timezone, datetime
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import InjectDB, User
from sqlalchemy.sql import select
from sqlalchemy.exc import NoResultFound
from passlib.context import CryptContext
from configs import JWT_SECRET_KEY

auth_router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class LoginPayload(BaseModel):
    email: str
    password: str
    # TODO: implement CSRF token validation


class RegisterPayload(BaseModel):
    email: str
    password: str
    fullname: str


def verify_pwd(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_pwd_hash(plain: str) -> str:
    return pwd_context.hash(plain)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    exp = datetime.now(timezone.utc) + expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": exp})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY)
    return encoded_jwt


@auth_router.post("/login")
async def login(payload: LoginPayload, db: InjectDB):
    try:
        async with db:
            q = select(User).where(User.email == payload.email)
            result = await db.session.execute(q)
            user = result.scalar_one_or_none()

        if not user:
            return JSONResponse({"message": f"No user found with email: {payload.email}"}, 401)

        if not verify_pwd(payload.password, user.password):
            return JSONResponse({"message": "Invalid password"}, 401)

        return JSONResponse({}, 200)
    except NoResultFound:
        return JSONResponse({"message": f"No user found with email {payload.email}"}, 401)
    except Exception as e:
        return JSONResponse({"message": str(e)}, 500)


@auth_router.post("/register")
async def register(payload: RegisterPayload, db: InjectDB):
    return None


# TODO:
@auth_router.post("/logout")
async def logout(db: InjectDB):
    return None
