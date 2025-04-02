from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.keyboards.callback_data import ShopMenuCallback, AdminCallback
from tg_bot.keyboards.keyboard import admin_kb, main_menu_kb
from tg_bot.services.shop_manager import ShopManager
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message


class ProductsStates(StatesGroup):
    AddProducts = State()


router = Router()


@router.callback_query(AdminCallback.filter(F.action == "view"))
async def show_admin(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ProductsStates.AddProducts)
    await callback.message.edit_text(text=f"Введите данные через пробел: название,категория,количество,цена ",
                                      reply_markup=None)


@router.message(ProductsStates.AddProducts)
async def get_data_from_states(message: Message, state: FSMContext):
    data = message.text.split(' ')
    data = [int(i) if i.isdigit() else i for i in data]
    result = {'product':data[0],
              'category':data[1],
              'quantity':data[2],
              'price':data[3]}
    await ShopManager.add_data(**result)
    await message.answer(text=f"ваши даннык получены {data}", reply_markup=admin_kb())
    await state.clear()


@router.callback_query(AdminCallback.filter(F.action == "back"))
async def show_admin(callback: CallbackQuery):
    await callback.message.edit_text(
        "Меню",
        reply_markup=main_menu_kb(),
    )
