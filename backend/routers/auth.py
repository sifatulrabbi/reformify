from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from crud.users import create_user, get_user_by_email, trim_user
from database import DBSessionDep
from auth import hash_pwd, verify_pwd, create_access_token


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

    if not verify_pwd(payload.password, user.password):
        raise HTTPException(401, "Incorrect password please try again.")

    access_token = create_access_token({"sub": user.id, "email": user.email})

    return {
        "user": trim_user(user),
        "access_token": access_token,
    }


@auth_router.post("/register")
async def register(payload: RegisterPayload, db_session: DBSessionDep):
    # TODO: include password and email validity check
    if not payload.email or not payload.password or not payload.fullname:
        raise HTTPException(
            400,
            "Invalid request payload. Please enclude 'email', 'password', and 'fullname'.",
        )

    try:
        existing_user = await get_user_by_email(db_session, payload.email)
        if existing_user:
            return JSONResponse(
                status_code=403,
                content={"message": "Email already in use please login."},
            )

        p = payload.model_dump()
        p["password"] = hash_pwd(p["password"])
        user = await create_user(db_session, p)
    except Exception as e:
        raise HTTPException(500, f"Unable to create the user due to: {e}")

    access_token = create_access_token({"sub": user.id, "email": user.email})

    return {
        "user": trim_user(user),
        "access_token": access_token,
    }
