from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from infrastructure.database import async_engine
from datetime import datetime


class Base(DeclarativeBase, AsyncAttrs):
    pass


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    product: Mapped[str] = mapped_column(String(100), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)
    action: Mapped[str] = mapped_column(default="view")
    price: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(),nullable=False)


class Balance(Base):
    __tablename__ = "balance"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True,primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger,unique=True,nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[int] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(),nullable=False)
    


class Support(Base):
    __tablename__ = "support"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(BigInteger,unique=True,nullable=False)
    full_name: Mapped[str] = mapped_column(String(100),nullable=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(),nullable=False)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)
