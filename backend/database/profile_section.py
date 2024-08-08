from uuid import uuid4
from sqlalchemy import UUID, Column, String
from . import Base


class ProfileSection(Base):
    __tablename__ = "profile_sections"
    __table_args__ = {"schema": "reformify"}

    id = Column(
        UUID(as_uuid=True), primary_key=True, default=uuid4(), unique=True, index=True
    )
    title = Column(String(length=256))
    # user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    # user = relationship("User", back_populates="sections")
