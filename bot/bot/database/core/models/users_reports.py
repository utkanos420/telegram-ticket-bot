from sqlalchemy import Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
import uuid
from .base import Base

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .users import User


class UserReport(Base):
    __tablename__ = "user_reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.user_id"), nullable=False)
    report_uuid: Mapped[str] = mapped_column(String, unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    report_floor: Mapped[int] = mapped_column(Integer, nullable=False)
    report_audience: Mapped[int] = mapped_column(Integer, nullable=False)
    report_reason: Mapped[str] = mapped_column(String, nullable=False)
    report_description: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)

    user: Mapped["User"] = relationship("User", back_populates="reports")
