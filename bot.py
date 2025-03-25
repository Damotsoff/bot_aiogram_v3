from aiogram import Bot, Dispatcher
from aiogram.types import Message
import betterlogging as bl
import asyncio
import logging
from tg_bot.config import load_config
from tg_bot.handlers.start import start_router
from tg_bot.handlers.budget import budget_router
from tg_bot.middlewares.errors import error_router


async def main():
    bl.basic_colorized_config(level=logging.INFO)
    config = load_config()
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()
    # dp.include_router(start_router)
    dp.include_router(budget_router)
    dp.include_router(error_router)

    await dp.start_polling(bot)
    await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot stopped!!")
