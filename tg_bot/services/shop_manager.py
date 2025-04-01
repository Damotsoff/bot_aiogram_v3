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
    async def get_beer(cls) -> Product | None:
        async with session_() as session:
            result = await session.execute(
                select(Product).where(Product.category == "beer")
            )
            if result:
                return result.scalars().all()
            
    @classmethod
    async def get_wine(cls) -> Product | None:
        async with session_() as session:
            result = await session.execute(
                select(Product).where(Product.category == "wine")
            )
            if result:
                return result.scalars().all()
            

    @classmethod
    async def get_spirits(cls) -> Product | None:
        async with session_() as session:
            result = await session.execute(
                select(Product).where(Product.category == "spirits")
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
            # Проверяем, есть ли уже данные
            existing_products = await session.execute(select(Product))
            if existing_products.scalars().first():
                print("Тестовые данные уже существуют")
                return

            products = [
                # Фрукты (старые данные)
                Product(product="Груши", category="fruits", quantity=5, price=250),
                Product(product="Яблоки", category="fruits", quantity=10, price=150),
                Product(product="Лимоны", category="fruits", quantity=10, price=350),
                Product(product="Апельсины", category="fruits", quantity=10, price=341),
                Product(product="Ананасы", category="fruits", quantity=10, price=500),
                
                # Овощи (старые данные)
                Product(product="Помидоры", category="vegetables", quantity=4, price=123),
                Product(product="Брокколи", category="vegetables", quantity=10, price=122),
                Product(product="Огурцы", category="vegetables", quantity=44, price=300),
                Product(product="Кукуруза", category="vegetables", quantity=44, price=300),
                
                # Пиво
                Product(product="Guinness Draught", category="beer", quantity=20, price=450, 
                    description="Ирландский стаут с кремовой текстурой"),
                Product(product="Heineken", category="beer", quantity=30, price=350,
                    description="Голландский светлый лагер"),
                Product(product="Балтика 9", category="beer", quantity=50, price=120,
                    description="Крепкое российское пиво"),
                Product(product="Hoegaarden", category="beer", quantity=15, price=400,
                    description="Бельгийское пшеничное пиво с цитрусовыми нотами"),
                
                # Вино
                Product(product="Château Margaux", category="wine", quantity=5, price=15000,
                    description="Французское красное вино премиум класса"),
                Product(product="Santa Margherita Pinot Grigio", category="wine", quantity=8, price=3200,
                    description="Итальянское белое сухое вино"),
                Product(product="Киндзмараули", category="wine", quantity=12, price=2500,
                    description="Грузинское полусладкое красное вино"),
                Product(product="Prosecco DOC", category="wine", quantity=18, price=1800,
                    description="Итальянское игристое вино"),
                
                # Крепкий алкоголь
                Product(product="Johnnie Walker Blue Label", category="spirits", quantity=3, price=25000,
                    description="Шотландский виски премиум класса"),
                Product(product="Beluga Noble", category="spirits", quantity=10, price=4500,
                    description="Российская премиальная водка"),
                Product(product="Havana Club 7", category="spirits", quantity=7, price=2800,
                    description="Кубинский выдержанный ром"),
                Product(product="Grey Goose", category="spirits", quantity=5, price=5200,
                    description="Французская люксовая водка из пшеницы"),
                Product(product="Hennessy VSOP", category="spirits", quantity=4, price=6800,
                    description="Коньяк премиум класса")
            ]

            session.add_all(products)
            await session.commit()
            print("Тестовые данные успешно добавлены")