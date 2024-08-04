from datetime import datetime, UTC
from sqlalchemy import CHAR, Column, String, Boolean, DATETIME
from .db import Base


def utctime():
    return datetime.now(UTC)


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "reformify"}

    id = Column(String, primary_key=True, unique=True, index=True)
    username = Column(CHAR)
    email = Column(String, index=True, unique=True)
    password = Column(String)
    created_at = Column(DATETIME, default=utctime)
    updated_at = Column(DATETIME, default=utctime, onupdate=utctime)
    deleted = Column(Boolean, default=False)
    profile = Column(String)


class Profile(Base):
    __tablname__ = "profiles"
    __table_args__ = {"schema": "reformify"}

    user = Column(String, primary_key=True, unique=True)
    fullname = Column(String)
