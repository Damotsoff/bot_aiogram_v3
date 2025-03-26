from aiogram import Router,types,F
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove
from tg_bot.keyboards.keyboard import menu


keyboard_router = Router()



@keyboard_router.message(Command("menu"))
async def send_menu(message: types.Message):
    await message.answer(
        "Выберите блюдо:",
        reply_markup=menu  # Прикрепляем клавиатуру
    )

@keyboard_router.message(F.text.as_('order'))
async def choose_food(message: types.Message, order:str):
    if order in ["Котлетки","Пюрешка","Макарошки"]:
        await message.answer(text=f"Вы выбрали {order}",reply_markup=ReplyKeyboardRemove())