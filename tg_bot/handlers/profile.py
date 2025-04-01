from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from tg_bot.keyboards.keyboard import profile_kb
from tg_bot.keyboards.callback_data import MainMenuCallback, ViewProfileCallback
from tg_bot.services.shop_manager import ShopManager


router = Router()


class StateBalance(StatesGroup):
    balance = State()

@router.callback_query(MainMenuCallback.filter(F.section == "profile"))
async def open_shop(callback: CallbackQuery):
    balance = await ShopManager.get_balance(callback.from_user.id)
    await callback.message.edit_text(
        f"ваш профиль:\n{callback.from_user.full_name}\n Ваш ID:{callback.from_user.id} \n Ваш баланс: {balance} RUB ",
        reply_markup=profile_kb(),
    )


@router.callback_query(ViewProfileCallback.filter(F.action == "view"))
async def view_balance(callback: CallbackQuery):
    balance = await ShopManager.get_balance(callback.from_user.id)
    await callback.message.edit_text(
        text=f"ваш баланс составляет {balance}",
        reply_markup=profile_kb(balance=balance),
    )



@router.message(StateBalance.balance)
async def write_balance(message:Message,state:FSMContext):
    balance = int(message.text)
    user_id = message.from_user.id
    full_name = message.from_user.full_name
    await ShopManager.add_user_id(user_id=user_id,balance=balance,full_name=full_name)
    await message.answer(text='Ваш баланс пополнен',reply_markup=profile_kb(balance=balance))
    await state.clear()



@router.callback_query(ViewProfileCallback.filter(F.action == 'balance'))
async def update_balance(callback:CallbackQuery,state:FSMContext):
    await callback.message.edit_text(text="Введите сумму :",reply_markup=None)
    await state.set_state(StateBalance.balance)
