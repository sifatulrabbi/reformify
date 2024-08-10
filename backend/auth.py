from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from configs import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from crud.users import get_user_by_id
from database import DBSessionDep
from database.user import BaseUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    exp = datetime.now(timezone.utc) + (
        expires_delta
        if expires_delta
        else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = data.copy()
    payload.update({"exp": exp})
    encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_pwd(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_pwd(plain: str) -> str:
    return pwd_context.hash(plain)


async def get_current_user(request: Request, db_session: DBSessionDep) -> BaseUser:
    auth_token = request.headers.get("Authorization")
    if not auth_token:
        raise HTTPException(401, "No access token found")
    [token_type, token] = auth_token.split(" ", 1)
    if token_type != "Bearer":
        raise HTTPException(401, "Invalid access token type")
    if not token:
        raise HTTPException(401, "Invalid access token")

    try:
        payload = jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if not payload.get("email") or not payload.get("sub"):
            raise HTTPException(401, "Invalid access token")
    except ExpiredSignatureError:
        raise HTTPException(401, "Access token has expired!")
    except InvalidTokenError as e:
        raise HTTPException(401, str(e))

    id = payload.get("sub")
    user = await get_user_by_id(db_session, id)
    if not user:
        raise HTTPException(401, "user not found")
    return user.serialize()


def require_auth(roles: list[str] = ["user"]):
    return Depends(get_current_user)


RequiredAuth = Annotated[BaseUser, require_auth()]
