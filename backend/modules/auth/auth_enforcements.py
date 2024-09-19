from typing import Annotated
from fastapi import Header
from fastapi.exceptions import HTTPException


def enforce_apikey_auth(x_reformify_api_key: Annotated[str | None, Header()]):
    if not x_reformify_api_key:
        raise HTTPException(401, "No api key found")
