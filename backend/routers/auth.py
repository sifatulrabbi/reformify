from fastapi import APIRouter
from pydantic import BaseModel
from database.db import InjectDB

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
    return None


@auth_router.post("/register")
async def register(payload: RegisterPayload, db: InjectDB):
    return None


# TODO:
@auth_router.post("/logout")
async def logout(db: InjectDB):
    return None
