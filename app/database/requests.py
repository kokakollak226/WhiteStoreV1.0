from app.database.models import async_session
from app.database.models import User, Admin
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import order, order_gold

async def check_lvl(session: AsyncSession, tg_id: int):
    query = select(Admin.lvl).where(Admin.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_add_admin(
        session: AsyncSession,
        tg_id: int,
        lvl: int,
        name: str,
        
):
    query = select(Admin).where(Admin.tg_id == tg_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            Admin(tg_id=tg_id, lvl=lvl, name=name))
        await session.commit()

async def delete_admin(session: AsyncSession, tg_id: int):
    query = delete(Admin).where(Admin.tg_id == tg_id)
    await session.execute(query)
    await session.commit()

async def check_adm(session: AsyncSession, tg_id: int):
    query = select(Admin).where(Admin.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()
    
async def adm_list(session: AsyncSession):
    query = select(Admin)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_add_user(
        session: AsyncSession,
        tg_id: int,
        balance: int,
        balance_gold: float,
        #gold_listing: float,
):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(tg_id=tg_id, balance=balance, balance_gold=balance_gold)) #gold_listing=gold_listing))
        await session.commit()

async def user_balance(
        session: AsyncSession,
        tg_id: int,
):
    query = select(User.balance).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def Profile(     
        session: AsyncSession,
        tg_id: int,
):
    query = select(User.id).where(User.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def Profiles(     
        session: AsyncSession,
):
    query = select(User.tg_id)
    result = await session.execute(query)
    return result.scalars().all()
    
async def orm_order_gold(session: AsyncSession, data: dict):
    ord_gold = order_gold(
        tg_name=data['tg_name'],
        tg_id=data['tg_id'],
        nick=data['nick'],
        price_gold=round(float(data['translate']), 2),
        screen_prof=data['screenshot_profile'],
        screen_skin=data['screenshot_skin']
        )
    session.add(ord_gold)
    await session.commit()

async def orm_get_orders_gold(session: AsyncSession):
    query = select(order_gold)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_orders_gold_id(session: AsyncSession, tg_id:int):
    query = select(order_gold).where(order_gold.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_orders_gold_error(session: AsyncSession, tg_id:int):
    query = select(order_gold.id).where(order_gold.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_order_gold(session: AsyncSession, order_id: int):
    query = select(order_gold).where(order_gold.id == order_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_balance_gold(session: AsyncSession, user_tg_id: int, balance_gold: float, balance: float):
    query = (
        update(User)
        .where(User.tg_id == user_tg_id)
        .values(
            tg_id=user_tg_id,
            balance_gold=User.balance_gold - balance_gold,
            balance= User.balance - int(balance),
            #gold_listing=User.gold_listing + balance_gold
        )
    )
    await session.execute(query)
    await session.commit()

async def delete_order_gold(session: AsyncSession, order_id: int):
    query = delete(order_gold).where(order_gold.id == order_id)
    await session.execute(query)
    await session.commit()

async def delete_all_order_gold(session: AsyncSession, order_tg_id: int):
    query = delete(order_gold).where(order_gold.tg_id == order_tg_id)
    await session.execute(query)
    await session.commit()

async def orm_order(session: AsyncSession, data: dict):
    ord = order(
        tg_name=data['tg_name'],
        tg_id=data['tg_id'],
        bank=data['bank'],
        price_gold=round(int(data['gold']) / 0.66, 2),
        price_rub=int(data['gold']),
        image=data['image'],
        )
    session.add(ord)
    await session.commit()

async def orm_get_orders(session: AsyncSession):
    query = select(order)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_orders_id(session: AsyncSession, tg_id:int):
    query = select(order).where(order.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_order(session: AsyncSession, order_id: int):
    query = select(order).where(order.id == order_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_balance(session: AsyncSession, user_tg_id: int, balance: int):
    query = (
        update(User)
        .where(User.tg_id == user_tg_id)
        .values(
            tg_id=user_tg_id,
            balance=User.balance+balance,
            balance_gold= round(int(balance) / 0.66, 2)
        )
    )
    await session.execute(query)
    await session.commit()

async def delete_order(session: AsyncSession, order_id: int):
    query = delete(order).where(order.id == order_id)
    await session.execute(query)
    await session.commit()

async def delete_all_order(session: AsyncSession, order_tg_id: int):
    query = delete(order).where(order.tg_id == order_tg_id)
    await session.execute(query)
    await session.commit()