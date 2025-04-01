from sqlalchemy import select
from tg_bot.infrastructure.database import session_
from tg_bot.models.models import Balance, Product, Support


from random import randint


class ShopManager:
    @classmethod
    async def get_balance(cls, user_id: int) -> int:
        async with session_() as session:
            result = await session.execute(
                select(Balance.balance).where(Balance.user_id == user_id)
            )
            balance = result.scalars().first()
            if balance:
                return balance
            return False

    @classmethod
    async def get_fruits(cls) -> Product | None:
        async with session_() as session:
            result = await session.execute(
                select(Product).where(Product.category == "fruits")
            )
            if result:
                return result.scalars().all()

    @classmethod
    async def get_products(cls, id: int):
        async with session_() as session:
            result = await session.execute(select(Product).where(Product.id == id))
            if result:
                return result.scalars().first()

    @classmethod
    async def get_vegetables(cls) -> Product | None:
        async with session_() as session:
            result = await session.execute(
                select(Product).where(Product.category == "vegetables")
            )
            if result:
                return result.scalars().all()

    @classmethod
    async def update_products(cls, item_id: int):
        async with session_() as session:
            result = await session.execute(select(Product).where(Product.id == item_id))
            quantity = result.scalars().first()
            if quantity:
                quantity.quantity -= 1
            await session.commit()

    @classmethod
    async def update_balance(cls, user_id: int, amount: int):
        async with session_() as session:
            result = await session.execute(
                select(Balance).where(Balance.user_id == user_id)
            )
            balance = result.scalars().first()
            if balance:
                balance.balance -= amount
                await session.commit()

    @classmethod
    async def add_user_id(cls, user_id: int, full_name: str):
        async with session_() as session:
            user = await session.execute(
                select(Balance).where(Balance.user_id == user_id)
            )
            user = user.scalars().first()
            if user:
                return
            balance = Balance(
                user_id=user_id, balance=randint(1, 5000), full_name=full_name
            )
            session.add(balance)
            await session.commit()

    @classmethod
    async def add_ticket(cls, **kwargs):
        async with session_() as session:
            ticket = Support(**kwargs)
            session.add(ticket)
            await session.commit()

    @classmethod
    async def insert_sample_data(cls):
        async with session_() as session:
            # Вставка продуктов
            products = [
                Product(product="Груши", category="fruits", quantity=5, price=250),
                Product(product="Яблоки", category="fruits", quantity=10, price=150),
                Product(
                    product="Помидоры", category="vegetables", quantity=4, price=123
                ),
                Product(
                    product="Брокколи", category="vegetables", quantity=10, price=122
                ),
            ]

            # Вставка обращения в поддержку
            support = Support(
                user_id=123,
                text="Проблема с заказом",
            )

            # Добавляем все объекты в сессию
            session.add_all(products)
            # session.add(balance)
            session.add(support)

            # Фиксируем изменения
            await session.commit()
            print("Данные успешно добавлены")
