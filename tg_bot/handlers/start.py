from aiogram import F, Router, Bot
from aiogram.filters import Command
from aiogram import types
from tg_bot.config import load_config


ADMIN = load_config().tg_bot.admin

start_router = Router()


@start_router.message(F.from_user.id == ADMIN, F.text == "/admin")
async def is_admin(message: types.Message, bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="hello creator")
    await get_ids(message,bot)


@start_router.message(Command("myid"))
async def get_ids(message: types.Message,bot: Bot):
    await bot.send_message(chat_id=ADMIN,text=
        f"Ваш user_id: {message.from_user.id}\n" f"Chat ID: {message.chat.id}"
    )

