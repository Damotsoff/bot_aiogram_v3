from aiogram import Router,F
from aiogram.filters import Command
from aiogram import types
from aiogram.types import CallbackQuery
from tg_bot.keyboards.keyboard import choise
from tg_bot.keyboards.callback_data import BuyCallback
inline_router = Router()


@inline_router.message(Command("shop",prefix="/"))
async def show_shop(message: types.Message):
    print("Команда /shop получена!")
    await message.answer("Выберите товар:", reply_markup=choise)

# Обработка груш
@inline_router.callback_query(BuyCallback.filter(F.item_name == "pear"))
async def buy_pear(callback: CallbackQuery, callback_data: BuyCallback):
    await callback.answer(f"Груши ×{callback_data.quantity} в корзине!", show_alert=True)

# Обработка яблок
@inline_router.callback_query(BuyCallback.filter(F.item_name == "apple"))
async def buy_apple(callback: CallbackQuery, callback_data: BuyCallback):
    await callback.answer(f"Яблоки ×{callback_data.quantity} в корзине!", show_alert=True)

# Обработка отмены
@inline_router.callback_query(F.data == "cancel")
async def cancel(callback: CallbackQuery):
    await callback.answer("Отменено!", show_alert=True)
    await callback.message.delete()
