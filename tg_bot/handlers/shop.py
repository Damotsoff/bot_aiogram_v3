from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton,InlineKeyboardMarkup
from tg_bot.keyboards.callback_data import MainMenuCallback, ProductCallback, ShopMenuCallback
from tg_bot.keyboards.keyboard import fruits_menu_kb, main_menu_kb, shop_menu_kb
router = Router()

# Стартовая команда
@router.message(Command("test"))
async def start(message: Message):
    await message.answer(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )

# Обработка главного меню
@router.callback_query(MainMenuCallback.filter(F.section == "shop"))
async def open_shop(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите категорию:",
        reply_markup=shop_menu_kb()
    )

# Обработка меню магазина
@router.callback_query(ShopMenuCallback.filter(F.action == "list"))
async def show_category(callback: CallbackQuery, callback_data: ShopMenuCallback):
    if callback_data.category == "fruits":
        await callback.message.edit_text(
            "Фрукты в наличии:",
            reply_markup=fruits_menu_kb()
        )

# Возврат назад
@router.callback_query(ShopMenuCallback.filter(F.action == "back"))
async def back_to_main(callback: CallbackQuery):
    await callback.message.edit_text(
        "Главное меню:",
        reply_markup=main_menu_kb()
    )

# Просмотр товара
@router.callback_query(ProductCallback.filter(F.action == "view"))
async def view_product(callback: CallbackQuery, callback_data: ProductCallback):
    await callback.message.edit_text(
        f"Товар ID: {callback_data.item_id}\n\nЦена: 100 руб.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(
                text="Купить",
                callback_data=ProductCallback(item_id=callback_data.item_id, action="buy").pack()
            )],
            [InlineKeyboardButton(
                text="Назад",
                callback_data=ShopMenuCallback(category="fruits", action="list").pack()
            )]
        ])
    )