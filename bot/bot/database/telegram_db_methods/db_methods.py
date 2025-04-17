"""
Основной модуль обращений к бд, в дальнейшем в логике бота используются экземпляры от класса DBMethods
"""
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from database.core.models import User, UserReport
from database.core.models import db_helper
from datetime import datetime
import uuid


class DBMethods:
    def __init__(self):
        self.session = db_helper.get_scoped_session()

    async def get_user(self, user_id: int) -> User | None:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            return result.scalars().first()

    async def create_user(self, user_id: int, username: str) -> User:
        async with self.session() as session:
            user = User(user_id=user_id, user_username=username, users_reports_count=0)
            session.add(user)
            await session.commit()
            return user

    async def get_user_data(self, user_id: int):
        user = await self.get_user(user_id)
        profile = await self.get_profile(user_id)
        return user, profile

    async def create_user_report(
        self,
        user_id: int,
        report_floor: int,
        report_audience: int,
        report_reason: str,
        report_description: str = None
    ) -> UserReport:
        async with self.session() as session:
            new_report = UserReport(
                user_id=user_id,
                report_uuid=str(uuid.uuid4()),
                report_floor=report_floor,
                report_audience=report_audience,
                report_reason=report_reason,
                report_description=report_description,
                created_at=datetime.utcnow()
            )

            session.add(new_report)
            await session.commit()
            await session.refresh(new_report)
            return new_report

    async def get_user_report_by_id(self, report_id: int) -> UserReport | None:
        async with self.session() as session:
            result = await session.execute(
                select(UserReport)
                .options(joinedload(UserReport.user))
                .filter_by(id=report_id)
            )
            return result.scalars().first()

    async def mute_user_by_id(self, user_id: int) -> bool:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            user = result.scalars().first()

            if user is None:
                return False

            user.is_muted = True
            await session.commit()
            return True

    async def unmute_user_by_id(self, user_id: int) -> bool:
        async with self.session() as session:
            result = await session.execute(select(User).filter_by(user_id=user_id))
            user = result.scalars().first()

            if user is None:
                return False

            user.is_muted = False
            await session.commit()
            return True

    async def user_is_muted(self, user_id: int) -> bool:
        async with self.session() as session:
            result = await session.execute(select(User.is_muted).filter_by(user_id=user_id))
            is_muted = result.scalar()
            return bool(is_muted)
