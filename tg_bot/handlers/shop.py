from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command

from tg_bot.keyboards.callback_data import (
    MainMenuCallback,
    ProductCallback,
    ShopMenuCallback,
)
from tg_bot.keyboards.keyboard import (
    main_menu_kb,
    shop_menu_kb,
    purchased_kb,
)


from tg_bot.services.shop_manager import ShopManager

router = Router()


@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_kb())


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


@router.callback_query(ProductCallback.filter(F.action == "buy"))
async def purchased(callback: CallbackQuery, callback_data: ProductCallback):
    balance = await ShopManager.get_balance(callback.from_user.id)
    product = await ShopManager.get_products(id=callback_data.id)
    if product.quantity < 1:
        await callback.message.edit_text(
            text="Товар закончился", reply_markup=shop_menu_kb()
        )
    elif product.quantity >= 1 and balance >= callback_data.price:
        await ShopManager.update_products(callback_data.id)
        await ShopManager.update_balance(callback.from_user.id, callback_data.price)
        await callback.message.edit_text(
            text=f"Поздравляю Вы купили 1 {callback_data.product}.Остаток обновлен.",
            reply_markup=shop_menu_kb(),
        )
    else:
        await callback.message.edit_text(
            text="недостаточно средств", reply_markup=shop_menu_kb()
        )
        return
