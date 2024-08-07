from uuid import uuid4
from datetime import datetime, UTC
from sqlalchemy import CHAR, UUID, Column, String, Boolean, DATE, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


def utctime():
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "reformify"}

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True, index=True
    )
    email = Column(String(length=500), index=True, unique=True)
    fullname = Column(String(length=256))
    password = Column(String(length=256))
    created_at = Column(DATE, default=utctime)
    updated_at = Column(DATE, default=utctime, onupdate=utctime)
    deleted = Column(Boolean, default=False)
    # sections = relationship("ProfileSection", back_populates="user")


class ProfileSection(Base):
    __tablename__ = "profile_sections"
    __table_args__ = {"schema": "reformify"}

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True, index=True
    )
    title = Column(String(length=256))
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    # user = relationship("User", back_populates="sections")
