import os
from dotenv import load_dotenv, find_dotenv
from sqlalchemy import BigInteger, DateTime, Float, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession

load_dotenv(find_dotenv())
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))

async_session= async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    created: Mapped[DateTime] = mapped_column(DateTime, default=func.now())
    updated: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id = mapped_column(BigInteger, nullable=False)
    balance: Mapped[int] = mapped_column(BigInteger, nullable=False)

class order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    tg_name: Mapped[str] = mapped_column(String(60), nullable=False)
    bank: Mapped[str] = mapped_column(String(50), nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_rub: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(150))

class order_gold(Base):
    __tablename__ = 'order_gold'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[str] = mapped_column(BigInteger, nullable=False)
    price_gold: Mapped[float] = mapped_column(Float(asdecimal=True), nullable=False)
    price_rub: Mapped[int] = mapped_column(Integer, nullable=False)
    image: Mapped[str] = mapped_column(String(150))

    
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)