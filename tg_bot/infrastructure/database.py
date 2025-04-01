from config import load_config
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    AsyncSession,
    create_async_engine,
    AsyncAttrs,
)

DATABASE_URL = load_config().tg_bot.database_url


async_engine = create_async_engine(DATABASE_URL, pool_size=5, echo=True)

session_ = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)
