import jwt
from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from configs import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from crud.users import get_user_by_id


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# TODO: refactor the auth service using only functions
# some of these functions should also take in db_session: AsyncSession


class AuthService:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ) -> str:
        exp = (
            datetime.now(timezone.utc) + expires_delta
            if expires_delta
            else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        payload = data.copy()
        payload.update({"exp": exp})
        encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY)
        return encoded_jwt

    async def verify_pwd(self, plain: str, hashed: str) -> bool:
        return self.pwd_context.verify(plain, hashed)

    async def hash_pwd(self, plain: str) -> str:
        return self.pwd_context.hash(plain)

    async def get_current_user(self, token: Annotated[str, Depends(oauth2_scheme)]):
        credentials_exception = HTTPException(
            401, "Could not validate the token", {"WWW-Authenticate": "Bearer"}
        )
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY)
            if not payload.get("email") or not payload.get("sub"):
                raise credentials_exception
        except InvalidTokenError as e:
            raise credentials_exception
        except Exception as e:
            raise e

        id = payload.get("sub")
        user = await get_user_by_id(id)
        if not user:
            raise HTTPException(401, "user not found")
        return user
