from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from pydantic import BaseModel
from crud.users import get_user_by_email
from database import DBSessionDep


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
async def login(payload: LoginPayload, db_session: DBSessionDep):
    if not payload.email or not payload.password:
        raise HTTPException(400, "Invalid request payload")

    user = await get_user_by_email(db_session, payload.email)
    if not user:
        raise HTTPException(404, "No user found with the email please register.")
    return {"user": user.model_dump()}


@auth_router.post("/register")
async def register(payload: RegisterPayload, db_session: DBSessionDep): ...
