from typing import List
from datetime import datetime
from uuid import uuid4, UUID
from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID as SqlUUID, String, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import Base


class ProfileSection(Base):
    __tablename__ = "profile_sections"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True),
        primary_key=True,
        unique=True,
        default=uuid4,
    )
    title: Mapped[str] = mapped_column(String(length=256), nullable=False)
    user_id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True), ForeignKey("reformify.users.id"), nullable=False
    )
    user: Mapped[List["User"]] = relationship(back_populates="sections")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def __init__(self, *, user_id: UUID, title: str):
        self.title = title
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def serialize(self):
        return BaseProfileSection(**self.to_dict())


class BaseProfileSection(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
