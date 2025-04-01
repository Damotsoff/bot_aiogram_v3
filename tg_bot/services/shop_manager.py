from sqlalchemy import select
from sqlalchemy.orm import joinedload
from tg_bot.infrastructure.database import session_
from tg_bot.models.models import Balance, History, Product, Support


from random import randint


class ShopManager:

    @classmethod
    async def sum_history(cls, user_id: int):
        async with session_() as session:
            result = await session.execute(
                select(History.price).where(History.user_id == user_id)
            )
            if result:
                return sum(result.scalars().all())
            return None

    @classmethod
    async def get_history(cls, user_id: int):
        async with session_() as session:
            result = await session.execute(
                select(History)
                .where(History.user_id == user_id)
                .options(joinedload(History.product))
            )
            history = result.scalars().all()
            if not history:
                return None
            formatted_history = []
            for entry in history:
                formatted_entry = {
                    "id": entry.id,
                    "name": entry.product.product,
                    "quantity": entry.quantity,
                    "price": entry.price,
                    "purchased_at": entry.purchased_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                formatted_history.append(formatted_entry)

            return formatted_history

    @classmethod
    async def add_history(cls, **kwargs):
        async with session_() as session:
            history_entry = History(**kwargs)
            session.add(history_entry)
            await session.commit()
            await session.refresh(history_entry)

    @classmethod
    async def get_balance(cls, user_id: int) -> int:
        async with session_() as session:
            result = await session.execute(
                select(Balance.balance).where(Balance.user_id == user_id)
            )
            balance = result.scalars().first()
            if balance:
                return balance
            return 0

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
            return 0

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
    async def update_balance(cls, user_id: int, amount: float):
        async with session_() as session:
            result = await session.execute(
                select(Balance).where(Balance.user_id == user_id)
            )
            balance = result.scalars().first()
            if balance:
                balance.balance -= amount
                await session.commit()

    @classmethod
    async def add_user_id(cls, user_id: int, full_name: str, balance: int):
        async with session_() as session:
            user = await session.execute(
                select(Balance).where(Balance.user_id == user_id)
            )
            user = user.scalars().first()
            if user:
                user.balance = balance
                await session.commit()
                return
            balance = Balance(user_id=user_id, balance=balance, full_name=full_name)
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
            products = [
                Product(product="Груши", category="fruits", quantity=5, price=250),
                Product(product="Яблоки", category="fruits", quantity=10, price=150),
                Product(
                    product="Помидоры", category="vegetables", quantity=4, price=123
                ),
                Product(
                    product="Брокколи", category="vegetables", quantity=10, price=122
                ),
                Product(product="Лимоны", category="fruits", quantity=10, price=350),
                Product(product="Апельсины", category="fruits", quantity=10, price=341),
                Product(product="Ананасы", category="fruits", quantity=10, price=500),
                Product(
                    product="Огурцы", category="vegetables", quantity=44, price=300
                ),
                Product(
                    product="Кукуруза", category="vegetables", quantity=44, price=300
                ),
            ]

            session.add_all(products)
            await session.commit()
            print("Данные успешно добавлены")
