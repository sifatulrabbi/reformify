from typing import Annotated
import jwt
from fastapi import Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from pydantic import BaseModel, ConfigDict, Field, ValidationError
from configs import JWT_SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES
from passlib.context import CryptContext
from datetime import timedelta, timezone, datetime
from crud.users import get_user_by_id
from database import DBSessionDep
from database.user import BaseUser


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGORITHM = "HS256"


class AccessToken(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sub: str
    email: str
    exp: datetime = Field(
        default=datetime.now(timezone.utc)
        + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    access_token = AccessToken.model_validate(data)
    if expires_delta:
        access_token.exp = datetime.now(timezone.utc) + (expires_delta)
    encoded_jwt = jwt.encode(
        payload=access_token.model_dump(), key=JWT_SECRET_KEY, algorithm=ALGORITHM
    )
    return encoded_jwt


def verify_pwd(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def hash_pwd(plain: str) -> str:
    return pwd_context.hash(plain)


def validate_access_token(authorization: Annotated[str, Header()]) -> AccessToken:
    if not authorization or not isinstance(authorization, str):
        raise HTTPException(401, "No access token found")

    [token_type, token] = authorization.split(" ", 1)
    if token_type != "Bearer":
        raise HTTPException(401, "Invalid access token type")
    if not token:
        raise HTTPException(401, "Invalid access token")

    try:
        payload = jwt.decode(jwt=token, key=JWT_SECRET_KEY, algorithms=[ALGORITHM])
        access_token = AccessToken.model_validate(payload)
        return access_token
    except ExpiredSignatureError:
        raise HTTPException(401, "Access token has expired!")
    except InvalidTokenError as e:
        raise HTTPException(401, f"Invalid access token: {e}")
    except ValidationError:
        raise HTTPException(401, "Malformatted access token")
    except Exception as e:
        raise HTTPException(500, str(e))


async def get_current_user(
    authorization: Annotated[str, Header()], db_session: DBSessionDep
) -> BaseUser:
    if not authorization or not isinstance(authorization, str):
        raise HTTPException(401, "No access token found")

    [token_type, token] = authorization.split(" ", 1)
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
        raise HTTPException(401, f"Invalid access token: {e}")
    except Exception as e:
        raise HTTPException(500, str(e))

    id = payload.get("sub")
    user = await get_user_by_id(db_session, id)
    if not user:
        raise HTTPException(401, "user not found")
    return user.serialize()


def require_auth(skip_fetch=False):
    return Depends(validate_access_token) if skip_fetch else Depends(get_current_user)


RequiredAuth = Annotated[AccessToken, require_auth(True)]
RequiredUser = Annotated[BaseUser, require_auth(False)]
