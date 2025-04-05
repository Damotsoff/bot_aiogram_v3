from uuid import uuid4
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.markdown import hlink
from tg_bot.data.items import items
from tg_bot.keyboards.keyboard import main_menu_kb
from tg_bot.keyboards.purchases import buy_keyboard, check_transa_kb
from tg_bot.keyboards.callback_data import (
    BuyItemCallback,
    ShopMenuCallback,
    CheckTransaCallback,
)
from tg_bot.misc.qiwi import Payment

router = Router()


class Pay(StatesGroup):
    AddPayment = State()


@router.callback_query(
    ShopMenuCallback.filter((F.action == "list") & (F.category == "books"))
)
async def show_items(callback: CallbackQuery):
    caption = """
Название продукта : {title}
<i>Описание:</i>
{description}
<u>Цена</u> {price:.2f} <b>RUB</b>
            """
    for item in items:
        await callback.message.answer_photo(
            photo=item.photo,
            caption=caption.format(
                title=item.title, description=item.description, price=item.price
            ),
            reply_markup=buy_keyboard(
                item_id=item.id,
            ),
            parse_mode="HTML",
        )


@router.callback_query(BuyItemCallback.filter(F.action == "buy"))
async def create_invoice(
    callback: CallbackQuery, callback_data: BuyItemCallback, state: FSMContext
):
    await callback.answer(cache_time=60)
    pay_id = str(uuid4())
    item_id = int(callback_data.item_id) - 1
    item = items[item_id]
    price = item.price
    payment = Payment(price=price, pay_id=pay_id, id=item.id)
    await state.set_state(Pay.AddPayment)
    await state.update_data(payment=payment)
    link = payment.create()
    await callback.message.answer(text=f"{hlink('Ссылка на оплату! После оплаты нажми кнопку - "Оплатил"',url=link)}", reply_markup=check_transa_kb(),parse_mode="HTML")


@router.callback_query(Pay.AddPayment, CheckTransaCallback.filter(F.action == "buy"))
async def buy_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")

    try:
        result = payment.check_payment()
        if result=='success':
            item = items[payment.id - 1]
            path = item.path
            await callback.message.answer("Успешо! Немного подожи я сейчас пришлю книгу!")
            await callback.message.answer_document(document=FSInputFile(path),caption="Твоя книга!")
            await callback.message.answer(text='menu',reply_markup=main_menu_kb())
            await state.clear()
    except ValueError:
        await callback.message.answer("Транзакция не найдена.Нажми на проверку немного позже")
        return

@router.callback_query(Pay.AddPayment, CheckTransaCallback.filter(F.action == "cancel"))
async def buy(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text='menu',reply_markup=main_menu_kb())
