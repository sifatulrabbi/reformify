if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import asyncio
from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[str] = mapped_column(primary_key=True, index=True, unique=True)
    email: Mapped[str] = mapped_column(index=True, unique=True)
    password: Mapped[str]
    fullname: Mapped[str] = mapped_column(String(100))
    careers: Mapped[Optional[List["UserCareer"]]] = relationship(back_populates="user")


class UserCareer(Base):
    __tablename__ = "user_careers"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[str] = mapped_column(unique=True, index=True, primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    start_date: Mapped[str]
    end_date: Mapped[str | None] = mapped_column(default=None)
    user_id: Mapped[str] = mapped_column(ForeignKey("reformify.user_profiles.id"))
    user: Mapped["UserProfile"] = relationship(back_populates="careers")


async def run_tests():
    pass


if __name__ == "__main__":
    asyncio.run(run_tests())
