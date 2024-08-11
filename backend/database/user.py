from typing import List
from uuid import uuid4, UUID
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy import ARRAY, DateTime, String, func, UUID as SqlUUID, ForeignKey, null
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class BaseUserCareer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    company: str
    company_location: str
    job_type: str
    job_location: str
    company_description: str
    description: list[str] = Field(default=[])
    start_date: datetime
    end_date: datetime | None = Field(default=None)


class UserCareer(BaseUserCareer):
    id: UUID
    user_id: UUID


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    email: str
    fullname: str
    created_at: datetime
    careers: list[UserCareer]


class UserPrivate(User):
    password: str
    deleted: bool = Field(False)
    updated_at: datetime


class UserModel(Base):
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
    # sections: Mapped[List["ProfileSection"]] = relationship(back_populates="user")
    careers: Mapped[List["UserCareerModel"]] = relationship(back_populates="user")
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
            "careers": self.careers,
            "created_at": self.created_at,
        }

    def to_dict_full(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "fullname": self.fullname,
            "careers": self.careers,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "deleted": self.deleted,
            "password": self.password,
        }

    def serialize(self):
        return User(**self.to_dict())

    def serialize_full(self):
        return UserPrivate.model_validate(self.to_dict_full())


class UserCareerModel(Base):
    __tablename__ = "careers"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True), primary_key=True, unique=True, default=uuid4
    )
    user_id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True), ForeignKey("reformify.users.id"), nullable=False
    )
    user: Mapped["UserModel"] = relationship(back_populates="careers")
    title: Mapped[str] = mapped_column(String(length=100), nullable=False)
    company: Mapped[str] = mapped_column(String(length=100), nullable=False)
    company_location: Mapped[str] = mapped_column(String(length=100), nullable=False)
    job_type: Mapped[str] = mapped_column(String(length=50), nullable=False)
    job_location: Mapped[str] = mapped_column(String(length=100), nullable=False)
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    company_description: Mapped[str] = mapped_column(String(length=400))
    description: Mapped[list[str]] = mapped_column(ARRAY(String))

    def __init__(
        self,
        *,
        user_id: UUID,
        title: str,
        company: str,
        job_type: str,
        start_date: datetime,
        description: list[str],
        company_description: str = "",
        job_location: str = "",
        company_location: str = "",
        end_date: datetime | None = None,
    ):
        if (
            not user_id
            or not title
            or not company
            or not job_type
            or not description
            or not company_location
            or not start_date
        ):
            raise Exception("Can't create a new career entry with insufficiant data")

        self.user_id = user_id
        self.title = title
        self.company = company
        self.company_location = company_location
        self.job_type = job_type
        self.job_location = job_location
        self.start_date = start_date
        self.end_date = end_date
        self.description = description
        self.company_description = company_description

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "company": self.company,
            "company_location": self.company_location,
            "job_type": self.job_type,
            "job_location": self.job_location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "company_description": self.company_description,
            "description": self.description,
        }

    def serialize(self):
        return UserCareer.model_validate(self.to_dict())
