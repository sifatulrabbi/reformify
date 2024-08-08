from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import InjectDB
from sqlalchemy.exc import NoResultFound
from services.auth import AuthService
from services.users import UsersService


auth_router = APIRouter(prefix="/auth", tags=["auth"])


class LoginPayload(BaseModel):
    email: str
    password: str
    # TODO: implement CSRF token validation


class RegisterPayload(BaseModel):
    email: str
    password: str
    fullname: str


@auth_router.post("/login")
async def login(payload: LoginPayload, db: InjectDB):
    users_service = UsersService(db)
    auth_service = AuthService(users_service)


@auth_router.post("/register")
async def register(payload: RegisterPayload, db: InjectDB):
    users_service = UsersService(db)
    auth_service = AuthService(users_service)
    return None


# TODO:
@auth_router.post("/logout")
async def logout(db: InjectDB):
    return None
