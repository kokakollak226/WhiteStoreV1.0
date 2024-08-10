from app.database.models import Banned, Course, all_order, all_order_gold, async_session, yes_order, yes_order_gold
from app.database.models import User, Admin
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.models import order, order_gold

async def user_list(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()

async def check_lvl(session: AsyncSession, tg_id: int):
    query = select(Admin.lvl).where(Admin.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def check_ban(session: AsyncSession, tg_id: int):
    query = select(Banned).where(Banned.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def check_banned(session: AsyncSession):
    query = select(Banned)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_ban(
        session: AsyncSession,
        tg_id: int,
        name: str,
        balance: int,
        what_ban: str
        
):
    query = select(Banned).where(Banned.tg_id == tg_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            Banned(tg_id=tg_id, name=name, balance=balance, what_ban=what_ban))
        await session.commit()

async def check_what_ban(
        session: AsyncSession,
        tg_id: int
        
):
    query = select(Banned.what_ban).where(Banned.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def user_balance_ban(
        session: AsyncSession,
        tg_id: int,
):
    query = select(Banned.balance).where(Banned.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def delete_ban(session: AsyncSession, tg_id: int):
    query = delete(Banned).where(Banned.tg_id == tg_id)
    await session.execute(query)
    await session.commit()

async def check_name_ban(session: AsyncSession, tg_id: int):
    query = select(Banned.name).where(Banned.tg_id == tg_id)
    result = await session.execute(query)
    return result.scalar()

async def check_name(session: AsyncSession, tg_id: int):
    query = select(User.name).where(User.tg_id == tg_id)
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

async def adm_id(session: AsyncSession):
    query = select(Admin.tg_id)
    result = await session.execute(query)
    return result.scalars().all()
    
async def adm_list(session: AsyncSession):
    query = select(Admin)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_add_user(
        session: AsyncSession,
        tg_id: int,
        name: str,
        balance: int,
        balance_gold: float,
):
    query = select(User).where(User.tg_id == tg_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(tg_id=tg_id, name=name, balance=balance, balance_gold=balance_gold)) 
        await session.commit()

async def delete_user(session: AsyncSession, tg_id: int):
    query = delete(User).where(User.tg_id == tg_id)
    await session.execute(query)
    await session.commit()

async def user_balance(
        session: AsyncSession,
        tg_id: int,
):
    query = select(User.balance_gold).where(User.tg_id == tg_id)
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
        course=data['gold_course'],
        price_gold=round(float(data['translate']), 2),
        screen_prof=data['screenshot_profile'],
        screen_skin=data['screenshot_skin']
        )
    session.add(ord_gold)
    await session.commit()

async def orm_all_order_gold(session: AsyncSession, data: dict):
    ord_gold = all_order_gold(
        tg_name=data['tg_name'],
        tg_id=data['tg_id'],
        nick=data['nick'],
        course=data['gold_course'],
        price_gold=round(float(data['translate']), 2),
        screen_prof=data['screenshot_profile'],
        screen_skin=data['screenshot_skin']
        )
    session.add(ord_gold)
    await session.commit()

async def orm_all_orders_gold(session: AsyncSession):
    query = select(all_order_gold)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_yes_order_gold(session: AsyncSession, order_verify: dict):
    ord_gold = yes_order_gold(
        tg_name=order_verify.tg_name,
        tg_id=order_verify.tg_id,
        nick=order_verify.nick,
        course=order_verify.course,
        price_gold=round(order_verify.price_gold, 2),
        screen_prof=order_verify.screen_prof,
        screen_skin=order_verify.screen_skin
        )
    session.add(ord_gold)
    await session.commit()

async def orm_yes_orders_gold(session: AsyncSession):
    query = select(yes_order_gold)
    result = await session.execute(query)
    return result.scalars().all()

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
        course=data['rub_course'],
        bank=data['bank'],
        price_gold=round(int(data['gold']) / await orm_check_course(session), 2),
        price_rub=int(data['gold']),
        image=data['image'],
        )
    session.add(ord)
    await session.commit()

async def orm_yes_order(session: AsyncSession, order_change: dict):
    ord = yes_order(
        tg_name=order_change.tg_name,
        tg_id=order_change.tg_id,
        course=order_change.course,
        bank=order_change.bank,
        price_gold=round(order_change.price_gold, 2),
        price_rub=int(order_change.price_rub),
        image=order_change.image,
        )
    session.add(ord)
    await session.commit()

async def orm_get_yes_orders(session: AsyncSession):
    query = select(yes_order)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_all_order(session: AsyncSession, data: dict):
    ord = all_order(
        tg_name=data['tg_name'],
        tg_id=data['tg_id'],
        course=data['rub_course'],
        bank=data['bank'],
        price_gold=round(int(data['gold']) / data['rub_course'], 2),
        price_rub=int(data['gold']),
        image=data['image'],
        )
    session.add(ord)
    await session.commit()

async def orm_get_all_orders(session: AsyncSession):
    query = select(all_order)
    result = await session.execute(query)
    return result.scalars().all()

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

async def orm_update_balance(session: AsyncSession, user_tg_id: int, balance: int, balance_gold: float):
    query = (
        update(User)
        .where(User.tg_id == user_tg_id)
        .values(
            tg_id=user_tg_id,
            balance=User.balance+balance,
            balance_gold=User.balance_gold+balance_gold
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

async def orm_add_course(
        session: AsyncSession,
        course: float
        
):
    query = select(Course).where(Course.id == 1)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            Course(course=course)) 
        await session.commit()

async def orm_check_course(
        session: AsyncSession,
):
    query = select(Course.course).where(Course.id==1)
    result = await session.execute(query)
    return result.scalar()

async def orm_check_course_order(
        session: AsyncSession,
        tg_id: int
):
    query = select(order.course).where(order.tg_id==tg_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_course(session: AsyncSession, course: float):
    query = (
        update(Course)
        .where(Course.id == 1)
        .values(
            course=course
        )
    )
    await session.execute(query)
    await session.commit()