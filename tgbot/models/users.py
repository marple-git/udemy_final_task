from typing import Optional, List

from sqlalchemy import Column, BigInteger, insert, String, update, Boolean, Integer, select, ForeignKey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from tgbot.services.db_base import Base


class User(Base):
    __tablename__ = "users"
    chat_id = Column(BigInteger, primary_key=True)
    admin = Column(Boolean, default=False)
    allowed = Column(Boolean, default=False)
    balance = Column(Integer, default=0)

    @classmethod
    async def get_user(cls, session: AsyncSession, chat_id: int) -> 'User':
        async with session.begin():
            sql = select(cls).where(cls.chat_id == chat_id)
            request = await session.execute(sql)
            user: User = request.scalar()
        return user

    @classmethod
    async def add_user(cls, session: AsyncSession, chat_id: int) -> 'User':
        async with session.begin():
            sql = insert(cls).values(chat_id=chat_id).returning('*')
            result = await session.execute(sql)
            return result.first()

    @classmethod
    async def get_all_users(cls, session: AsyncSession) -> List['User']:
        async with session.begin():
            stmt = select(User.chat_id)
            result = await session.execute(stmt)
            return result.scalars().all()

    async def update_user(self, session: AsyncSession, updated_fields: dict, chat_id: Optional = None) -> 'User':
        chat_id = self.chat_id if not chat_id else chat_id
        async with session.begin():
            sql = update(User).where(User.chat_id == chat_id).values(**updated_fields)
            result = await session.execute(sql)
            return result

    def __repr__(self):
        return f'User (ID: {self.chat_id} - {self.admin} - {self.allowed})'
