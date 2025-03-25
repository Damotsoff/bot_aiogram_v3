from aiogram import F, Router, Bot
from aiogram import types
from aiogram.filters import Command
from aiogram.utils.deep_linking import create_start_link

start_router = Router()


@start_router.message(F.from_user.id == 399284082, F.text != "/start")
async def is_admin(message: types.Message):
    await message.answer("Hello my Creator!")


@start_router.message(Command("start", prefix="/!"))
async def start(message: types.Message, bot=Bot):
    link = await create_start_link(bot=bot, payload=f"ref-{message.from_user.id}")
    await bot.send_message(chat_id=message.chat.id, text=link)


@start_router.message(F.text)
async def start_handler(message: types.Message, bot: Bot):
    await bot.send_message(chat_id=message.chat.id, text=str(message.from_user.id))
