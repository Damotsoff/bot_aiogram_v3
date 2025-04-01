from datetime import datetime
from sqlalchemy import String, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs
from tg_bot.infrastructure.database import async_engine


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
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    description:Mapped[str] = mapped_column(nullable=True,default='test')

    purchases: Mapped[list["History"]] = relationship(back_populates="product")


class Balance(Base):
    __tablename__ = "balance"

    id: Mapped[int] = mapped_column(
        BigInteger, nullable=False, unique=True, primary_key=True
    )
    user_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    full_name: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[float] = mapped_column(default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)
    purchases: Mapped[list["History"]] = relationship(back_populates="user")


class History(Base):
    __tablename__ = "history"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger, ForeignKey("balance.user_id"), nullable=False
    )
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=True)
    price: Mapped[int] = mapped_column(nullable=True)
    purchased_at: Mapped[datetime] = mapped_column(
        default=datetime.now(), nullable=False
    )
    user: Mapped["Balance"] = relationship(back_populates="purchases")
    product: Mapped["Product"] = relationship(back_populates="purchases")


class Support(Base):
    __tablename__ = "support"

    id: Mapped[int] = mapped_column(
        BigInteger, primary_key=True, unique=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=False)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    text: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(), nullable=False)


async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all, checkfirst=True)


async def delete_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
