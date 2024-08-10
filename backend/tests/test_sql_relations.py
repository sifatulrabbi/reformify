if __name__ == "__main__":
    import os
    import sys

    parent_dir = os.path.join(os.path.dirname(__file__), "..")
    sys.path.append(parent_dir)


import asyncio
from icecream import ic
from datetime import datetime
from uuid import uuid4, UUID
from typing import List, Tuple, Union
from sqlalchemy import String, ForeignKey, func, UUID as SqlUUID, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select, update
from sqlalchemy.orm import Mapped, joinedload, mapped_column, relationship
from database import Base, sessionmanager


class UserProfile(Base):
    __tablename__ = "user_profiles"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid4
    )
    email: Mapped[str] = mapped_column(String, index=True, unique=True)
    password: Mapped[str] = mapped_column(String)
    fullname: Mapped[str] = mapped_column(String(100))
    careers: Mapped[List["UserCareer"]] = relationship(back_populates="user")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )


class UserCareer(Base):
    __tablename__ = "user_careers"
    __table_args__ = {"schema": "reformify"}

    id: Mapped[UUID] = mapped_column(
        SqlUUID(as_uuid=True), primary_key=True, index=True, unique=True, default=uuid4
    )
    title: Mapped[str] = mapped_column(String(200))
    start_date: Mapped[str] = mapped_column(String)
    end_date: Mapped[str | None] = mapped_column(default=None)
    user_id: Mapped[str] = mapped_column(ForeignKey("reformify.user_profiles.id"))
    user: Mapped["UserProfile"] = relationship(back_populates="careers")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


mock_user = {
    "id": "e304a3e7-0d02-468a-94a9-2124eec2c74e",
    "email": "sifatuli.r@gmail.com",
    "password": "password",
    "fullname": "Sifatul Rabbi",
}


async def get_user_by_id(session: AsyncSession, id: str) -> UserProfile | None:
    user = await session.scalar(
        select(UserProfile)
        .options(joinedload(UserProfile.careers))
        .where(UserProfile.id == id)
    )
    return user


async def update_user(session: AsyncSession, id: str, update_data: dict) -> None:
    await session.execute(
        update(UserProfile).where(UserProfile.id == id).values(**update_data)
    )
    await session.commit()


async def create_user(
    session: AsyncSession, *, email: str, password: str, fullname: str
) -> UserProfile | None:
    user = UserProfile(email=email, password=password, fullname=fullname)
    session.add(user)
    await session.commit()
    return user


async def create_user_career(
    session: AsyncSession,
    *,
    user_id: UUID,
    title: str,
    start_date: str,
    end_date: str | None
) -> UserCareer | None:
    career = UserCareer(
        title=title, start_date=start_date, end_date=end_date, user_id=user_id
    )
    session.add(career)
    await session.commit()
    return career


async def run_tests() -> None:
    async with sessionmanager.session() as session:
        user = await get_user_by_id(session, mock_user["id"])
        if user is None:
            raise Exception("Unable to find the user in the database.")
        ic([c.to_dict() for c in user.careers])

        # careers = [
        #     UserCareer(
        #         user_id=user.id,
        #         title="Software Engineer",
        #         start_date="2021-01-01",
        #         end_date="2023-01-01",
        #     ),
        #     UserCareer(
        #         user_id=user.id,
        #         title="Senior Software Engineer",
        #         start_date="2023-02-01",
        #         end_date=None,
        #     ),
        # ]
        # session.add_all(careers)
        # await session.commit()


if __name__ == "__main__":
    asyncio.run(run_tests())
