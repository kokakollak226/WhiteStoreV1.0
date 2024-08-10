import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import BigInteger, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

load_dotenv(find_dotenv())
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session= async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class Course(Base):
    __tablename__ = 'Course'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(150))
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
    balance_gold:  Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    #gold_listing: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)

class Admin(Base):
    __tablename__ = 'admin'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    lvl: Mapped[int] = mapped_column(Integer, nullable=False)
    name: Mapped[str] = mapped_column(String(70), nullable=False)
    
class Banned(Base):
    __tablename__ = 'banned'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False)
    what_ban: Mapped[str] = mapped_column(String(150))
    
class order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    bank: Mapped[str] = mapped_column(String(50), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_rub: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)

class order_gold(Base):
    __tablename__ = 'order_gold'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    nick: Mapped[str] = mapped_column(String(60))
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    screen_prof: Mapped[str] = mapped_column(String(150))
    screen_skin: Mapped[str] = mapped_column(String(150))

class yes_order_gold(Base):
    __tablename__ = 'yes_order_gold'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    nick: Mapped[str] = mapped_column(String(60))
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    screen_prof: Mapped[str] = mapped_column(String(150))
    screen_skin: Mapped[str] = mapped_column(String(150))

class all_order_gold(Base):
    __tablename__ = 'all_order_gold'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    nick: Mapped[str] = mapped_column(String(60))
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    screen_prof: Mapped[str] = mapped_column(String(150))
    screen_skin: Mapped[str] = mapped_column(String(150))

class yes_order(Base):
    __tablename__ = 'yes_order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    bank: Mapped[str] = mapped_column(String(50), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_rub: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)

class all_order(Base):
    __tablename__ = 'all_order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    course: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    bank: Mapped[str] = mapped_column(String(50), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_rub: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(150), nullable=False)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)