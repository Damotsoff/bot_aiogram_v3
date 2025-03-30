from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tg_bot.keyboards.callback_data import (
    MainMenuCallback,
    ProductCallback,
    ShopMenuCallback,
    ViewProfileCallback,
    SupportCallback,
)
from tg_bot.keyboards.keyboard import (
    fruits_menu_kb,
    main_menu_kb,
    shop_menu_kb,
    vegetables_menu_kb,
    profile_kb,
    support_kb,
    purchased_kb,
)

from tg_bot.keyboards.keyboard import product_storage, bank

router = Router()


@router.message(Command("test"))
async def start(message: Message):
    await message.answer("Главное меню:", reply_markup=main_menu_kb())


@router.callback_query(MainMenuCallback.filter(F.section == "shop"))
async def open_shop(callback: CallbackQuery):
    await callback.message.edit_text("Выберите категорию:", reply_markup=shop_menu_kb())


@router.callback_query(MainMenuCallback.filter(F.section == "profile"))
async def open_shop(callback: CallbackQuery):
    await callback.message.edit_text(
        f"ваш профиль:\n{callback.from_user.full_name}\n Ваш ID:{callback.from_user.id}",
        reply_markup=profile_kb(),
    )


@router.callback_query(MainMenuCallback.filter(F.section == "support"))
async def support(callback: CallbackQuery):

    await callback.message.edit_text(
        "Support", reply_markup=support_kb(callback.from_user.id)
    )


@router.callback_query(ViewProfileCallback.filter(F.action == "view"))
async def view_balance(callback: CallbackQuery, callback_data: ViewProfileCallback):
    await callback.message.edit_text(
        text=f"ваш баланс составляет {callback_data.balance}", reply_markup=profile_kb()
    )


@router.callback_query(ShopMenuCallback.filter(F.action == "list"))
async def show_category(callback: CallbackQuery, callback_data: ShopMenuCallback):
    if callback_data.category == "fruits":
        await callback.message.edit_text(
            "Фрукты в наличии:", reply_markup=fruits_menu_kb()
        )
    elif callback_data.category == "vegetables":
        await callback.message.edit_text(
            "Овощи в наличии:", reply_markup=vegetables_menu_kb()
        )


@router.callback_query(ShopMenuCallback.filter(F.action == "back"))
async def back_to_categories(callback: CallbackQuery):
    await callback.message.edit_text("Категории магазина:", reply_markup=shop_menu_kb())


@router.callback_query(MainMenuCallback.filter(F.action == "back"))
async def back_to_main_menu(callback: CallbackQuery):
    await callback.message.edit_text("Главная: ", reply_markup=main_menu_kb())


@router.callback_query(ProductCallback.filter(F.action == "view"))
async def view_product(callback: CallbackQuery, callback_data: ProductCallback):
    await callback.message.edit_text(
        f"Товар ID: {callback_data.item_id}\n\nЦена: {callback_data.price} руб.",
        reply_markup=purchased_kb(callback_data=callback_data),
    )


@router.callback_query(ProductCallback.filter(F.action == "buy"))
async def purchased(callback: CallbackQuery, callback_data: ProductCallback):

    if product_storage[callback_data.category][callback_data.product]["quantity"] < 1:
        await callback.message.edit_text(
            text="Товар закончился", reply_markup=shop_menu_kb()
        )
    elif (
        product_storage[callback_data.category][callback_data.product]["quantity"] >= 1
        and bank["balance"] >= callback_data.price
    ):
        product_storage[callback_data.category][callback_data.product]["quantity"] -= 1
        bank["balance"] -= callback_data.price
        await callback.message.edit_text(
            text=f"Поздравляю Вы купили 1 {callback_data.product}.Остаток обновлен.",
            reply_markup=shop_menu_kb(),
        )
    else:
        await callback.message.answer(text="недостаточно средств")
        return


class SupportStates(StatesGroup):
    waiting_for_support_text = State()


@router.message(SupportStates.waiting_for_support_text)
async def process_support_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    support_text = message.text

    await message.answer(
        text="🆘 Новое обращение:\n"
        f"👤 User ID: {user_id}\n"
        f"📄 Текст: {support_text}",
    )

    await message.answer(
        "✅ Ваше обращение отправлено! Спасибо.",
        reply_markup=support_kb(user_id),
    )

    await state.clear()


@router.callback_query(SupportCallback.filter(F.action == "create_ticket"))
async def handle_support_request(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.message.answer(text="📝 Опишите вашу проблему:", reply_markup=None)
    await state.set_state(SupportStates.waiting_for_support_text)

    # Подтверждаем обработку callback (убираем "часики" на кнопке)
    await callback.answer()
