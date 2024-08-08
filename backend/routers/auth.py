from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import InjectDB, User
from sqlalchemy.sql import select
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
    try:
        user = await users_service.get_by_email(payload.email)
        if not user:
            return JSONResponse({"message": f"No user found with email: {payload.email}"}, 401)
        if not auth_service.verify_pwd(payload.password, user.password):
            return JSONResponse({"message": "Invalid password"}, 401)
        token = await auth_service.create_access_token({"sub": user.id, "email": user.email})
        return JSONResponse({"user": user, "access_token": token, "token_type": "bearer"}, 200)
    except NoResultFound:
        return JSONResponse({"message": f"No user found with email {payload.email}"}, 401)
    except Exception as e:
        return JSONResponse({"message": str(e)}, 500)


@auth_router.post("/register")
async def register(payload: RegisterPayload, db: InjectDB):
    users_service = UsersService(db)
    auth_service = AuthService(users_service)
    return None


# TODO:
@auth_router.post("/logout")
async def logout(db: InjectDB):
    return None
