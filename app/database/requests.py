from app.database.models import async_session
from app.database.models import User
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import order, order_gold


async def set_user(tg_id, balance):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, balance=balance))
            await session.commit()

async def orm_order(session: AsyncSession, data: dict):
    ord = order(
        tg_id=data['id'],
        price_gold=round(int(data['gold']) / 0.66, 2),
        price_rub=int(data['gold']),
        image=data['image'],
        )
    session.add(ord)
    await session.commit()

#async def orm_get_order(session: AsyncSession, order_id:id):
    #query = select(order)
    #result = await session.execute(query)
    #return result.scalars().all