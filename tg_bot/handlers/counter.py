from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from tg_bot.keyboards.callback_data import MainMenuCallback, CounterCallback
from tg_bot.keyboards.keyboard import counter_kb, main_menu_kb
from tg_bot.services.shop_manager import ShopManager

router = Router()


class SetCounters(StatesGroup):
    AddPosition = State()
    AddItem = State()
    AddPrice = State()


@router.callback_query(MainMenuCallback.filter(F.section == "counter"))
async def counter(callback: CallbackQuery):
    await callback.message.edit_text("Couter хрючева:", reply_markup=counter_kb())


@router.callback_query(CounterCallback.filter(F.action == "create_count"))
async def get_posution(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(
        text="Что вы хотите добавить ? Напишите название", reply_markup=None
    )
    await state.set_state(SetCounters.AddItem)
    await callback.answer()


@router.callback_query(CounterCallback.filter(F.action == "view_count"))
async def view_results(callback: CallbackQuery):
    results = await ShopManager.view_position(callback.from_user.id)
    if results:
        formatted_history = []
        for entry in results:
            formatted_entry = (
                f"User ID: {entry['user_id']}\n"
                f"Имя: {entry['full_name']}\n"
                f"Название продукта: {entry['item']}\n"
                f"Количество: {entry['quantity']}\n"
                f"Цена за единицу: {entry['price']} руб.\n"
                f"Дата покупки: {entry['created_at']}\n"
                f"-----------------------------\n"
                f"Итого: {entry['total']}\n"
            )
            formatted_history.append(formatted_entry)
        answer = "\n".join(formatted_history)
        await callback.message.edit_text(text=f"{answer}", reply_markup=main_menu_kb())
        return
    await callback.message.edit_text(text='нет информации',reply_markup=main_menu_kb())


@router.message(SetCounters.AddItem)
async def add_item(message: Message, state: FSMContext):
    text = message.text
    await state.update_data(item_name=text)
    await message.answer("Сколько добавить? Напишите число:")
    await state.set_state(SetCounters.AddPosition)


@router.message(SetCounters.AddPosition)
async def add_position(message: Message, state: FSMContext):
    try:
        position = int(message.text)
        await state.update_data(quantity=position)
        await message.answer(
            "Если хотите можете указать цену(Если не хочешь просто введи любой символ)"
        )
        await state.set_state(SetCounters.AddPrice)
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число!")
        return


@router.message(SetCounters.AddPrice)
async def add_price(message: Message, state: FSMContext):
    try:
        user_id = message.from_user.id
        full_name = message.from_user.full_name
        price = message.text
        data = await state.get_data()
        item_name = data.get("item_name")
        position = data.get("quantity")
        price = int(price) if price.isdigit() else 0
        await ShopManager.add_position(
            user_id=user_id,
            full_name=full_name,
            item=item_name,
            quantity=position,
            price=price,
        )
        await message.answer(
            text=f"Спасибо! Вы добавили {position} единиц товара '{item_name}' , стоимость {price}.",
            reply_markup=main_menu_kb(),
        )
    except ValueError:
        await message.answer("Пожалуйста, введите корректное число!")
        return
    await state.clear()
