from pydantic import BaseModel, ConfigDict


class CreateUserPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str
    email: str
    image: str


class UpdateUserPayload(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    username: str | None
    email: str | None
    image: str | None
