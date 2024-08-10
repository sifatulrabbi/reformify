from typing import List
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import DateTime, String, func, UUID as SqlUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid4,
    )
    email: Mapped[str] = mapped_column(
        String(400), index=True, unique=True, nullable=False
    )
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False)
    sections: Mapped[List["ProfileSection"]] = relationship(back_populates="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def __init__(self, *, email: str, fullname: str, password: str):
        self.email = email
        self.fullname = fullname
        self.password = password

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def to_dict_full(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted": self.deleted,
            "password": self.password,
        }

    def serialize(self):
        return BaseUser(**self.to_dict())

    def serialize_full(self):
        return BaseUserPrivate(**self.to_dict_full())


class BaseUser(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    fullname: str
    created_at: datetime
    updated_at: datetime


class BaseUserPrivate(BaseUser):
    password: str
    deleted: bool = Field(False)
