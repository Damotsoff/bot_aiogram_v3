from aiogram import Bot, Dispatcher
import betterlogging as bl
import asyncio
import logging
from tg_bot.config import load_config
from tg_bot.handlers.budget import budget_router
from tg_bot.middlewares.errors import error_router
from tg_bot.handlers.shop import router as shop_router
from tg_bot.handlers.fruits import router as fruits_router
from tg_bot.handlers.vegetables import router as vegetables_router
from tg_bot.handlers.beer import router as beer_router
from tg_bot.handlers.wine import router as wine_router
from tg_bot.handlers.spirits import router as spirits_router
from tg_bot.handlers.profile import router as profile_router
from tg_bot.handlers.support import router as support_router
from tg_bot.handlers.counter import router as counter_router
from tg_bot.handlers.start import start_router
from tg_bot.models.models import create_tables, delete_tables
from tg_bot.services.shop_manager import ShopManager


async def main():
    # await delete_tables()
    await create_tables()
    # await ShopManager.insert_sample_data()
    bl.basic_colorized_config(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    dp.include_router(counter_router)
    dp.include_router(spirits_router)
    dp.include_router(wine_router)
    dp.include_router(beer_router)
    dp.include_router(start_router)
    dp.include_router(budget_router)
    dp.include_router(error_router)
    dp.include_router(shop_router)
    dp.include_router(fruits_router)
    dp.include_router(vegetables_router)
    dp.include_router(profile_router)
    dp.include_router(support_router)

    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!!")
