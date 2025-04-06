from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from tg_bot.config import load_config


from tg_bot.keyboards.callback_data import (
    MainMenuCallback,
    ProductCallback,
    ShopMenuCallback,
)
from tg_bot.keyboards.keyboard import main_menu_kb, shop_menu_kb, purchased_kb, admin_kb

ADMIN = load_config().tg_bot.admin
router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(MainMenuCallback.filter(F.section == "admin"))
async def open_shop(callback: CallbackQuery):
    if callback.from_user.id == ADMIN:
        await callback.message.edit_text("Админ панель:", reply_markup=admin_kb())


@router.callback_query(MainMenuCallback.filter(F.section == "shop"))
async def open_shop(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию:", reply_markup=shop_menu_kb())


@router.callback_query(ShopMenuCallback.filter(F.action == "back"))
async def back_to_categories(callback: CallbackQuery):
    await callback.message.edit_text("Категории магазина:", reply_markup=shop_menu_kb())


@router.callback_query(MainMenuCallback.filter(F.action == "back"))
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text("Главная: ", reply_markup=main_menu_kb())


@router.callback_query(ProductCallback.filter(F.action == "view"))
async def view_product(callback: CallbackQuery, callback_data: ProductCallback):
    await callback.message.edit_text(
        f"Товар ID: {callback_data.id}\n\nЦена: {callback_data.price} руб.",
        reply_markup=purchased_kb(callback_data=callback_data),
    )
