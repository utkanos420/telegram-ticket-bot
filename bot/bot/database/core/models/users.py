from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .users_reports import UserReport


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    is_muted: Mapped[bool] = mapped_column(Boolean, nullable=False, default=0, server_default="0")
    user_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    user_username: Mapped[str] = mapped_column(String, unique=False, nullable=False)
    users_reports_count: Mapped[int] = mapped_column(Integer, unique=False, nullable=True)

    reports: Mapped[list["UserReport"]] = relationship("UserReport", back_populates="user", cascade="all, delete-orphan")
