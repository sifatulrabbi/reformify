from pydantic import BaseModel, ConfigDict, Field
from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from . import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[str] = mapped_column(
        primary_key=True, unique=True, default=uuid4, nullable=False
    )
    email: Mapped[str] = mapped_column(index=True, unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False)

    def __init__(self, *, email: str, fullname: str, password: str):
        self.email = email
        self.fullname = fullname
        self.password = password

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
        }


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    fullname: str


class BaseUserPrivate(BaseUser):
    password: str
    deleted: bool
