from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.keyboards.keyboard import profile_kb
from tg_bot.keyboards.callback_data import MainMenuCallback, ViewProfileCallback
from tg_bot.services.shop_manager import ShopManager


router = Router()


@router.callback_query(MainMenuCallback.filter(F.section == "profile"))
async def open_shop(callback: CallbackQuery):
    # balance = await ShopManager.get_balance(callback.from_user.id)
    await callback.message.edit_text(
        f"ваш профиль:\n{callback.from_user.full_name}\n Ваш ID:{callback.from_user.id}",
        reply_markup=profile_kb(),
    )
    # await ShopManager.add_user_id(str(callback.from_user.id))


@router.callback_query(ViewProfileCallback.filter(F.action == "view"))
async def view_balance(callback: CallbackQuery):
    balance = await ShopManager.get_balance(callback.from_user.id)
    await callback.message.edit_text(
        text=f"ваш баланс составляет {balance}", reply_markup=profile_kb(balance=balance)
    )
