from decimal import Decimal
from typing import Union, List

from sqlalchemy import Column, insert, String, Integer, Numeric, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from tgbot.services.db_base import Base


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    description = Column(String(4096))
    photo = Column(String(250))
    price = Column(Numeric)

    def __repr__(self):
        return f'Item (ID: {self.id} | {self.name} | {self.price})'


async def add_item(name: str, description: str, photo: str, price: Union[int, Decimal], session: AsyncSession) -> Item:
    async with session.begin():
        stmt = insert(Item).values(name=name, description=description, photo=photo, price=price)
        result = await session.execute(stmt)
        item: Item = result.scalar()
    return item


async def get_items(session: AsyncSession, name: str = None) -> List[Item]:
    async with session.begin():
        if name:
            stmt = select(Item).where(Item.name.ilike(f'%{name}%'))
        else:
            stmt = select(Item).order_by(Item.name)
        result = await session.execute(stmt)
    return result.scalars().all()


async def get_item(session: AsyncSession, item_id: int) -> Item:
    async with session.begin():
        stmt = select(Item).where(Item.id == item_id)
        result = await session.execute(stmt)
    return result.scalar()
