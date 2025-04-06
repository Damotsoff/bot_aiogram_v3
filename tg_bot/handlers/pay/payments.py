from uuid import uuid4
from aiogram import Router, F
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.utils.markdown import hlink
from tg_bot.data.items import items
from tg_bot.keyboards.callback_data import ProductCallback
from tg_bot.services.shop_manager import ShopManager
from tg_bot.keyboards.keyboard import main_menu_kb
from tg_bot.keyboards.purchases import check_transa_kb
from tg_bot.states.states import Pay
from tg_bot.keyboards.callback_data import (
    BuyItemCallback,
    CheckTransaCallback,
)
from tg_bot.misc.yoomoney import Payment

router = Router()


@router.callback_query(BuyItemCallback.filter(F.action == "buy"))
async def create_invoice(
    callback: CallbackQuery, callback_data: BuyItemCallback, state: FSMContext
):
    await callback.answer(cache_time=60)
    pay_id = str(uuid4())
    item_id = int(callback_data.item_id)
    item = items[item_id]
    price = item.price
    payment = Payment(price=price, pay_id=pay_id, id=item.id)
    await state.set_state(Pay.AddPayment)
    await state.update_data(payment=payment)
    link = payment.create()
    await callback.message.answer(
        text=f"{hlink('Ссылка на оплату! После оплаты нажми кнопку - "Оплатил"',url=link)}",
        reply_markup=check_transa_kb(),
        parse_mode="HTML",
    )


@router.callback_query(Pay.AddPayment, CheckTransaCallback.filter(F.action == "buy"))
async def buy_item(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    payment: Payment = data.get("payment")

    try:
        result = payment.check_payment()
        if result == "success":
            item = items[payment.id - 1]
            path = item.path
            await callback.message.answer(
                "Успешо! Немного подожди я сейчас пришлю книгу!"
            )
            await callback.message.answer_document(
                document=FSInputFile(path), caption="Твоя книга!"
            )
            await callback.message.answer(text="menu", reply_markup=main_menu_kb())
            await state.clear()
    except ValueError:
        await callback.message.answer(
            "Транзакция не найдена.Нажми на проверку немного позже"
        )
        return


@router.callback_query(Pay.AddPayment, CheckTransaCallback.filter(F.action == "cancel"))
async def buy(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.answer(text="menu", reply_markup=main_menu_kb())


@router.callback_query(ProductCallback.filter(F.action == "buy"))
async def purchased(callback: CallbackQuery, callback_data: ProductCallback):
    balance = await ShopManager.get_balance(callback.from_user.id)
    product = await ShopManager.get_products(id=callback_data.id)
    assert balance >= 0, "Значение не может быть меньше нуля!"
    if not product:
        return
    if product.quantity < 1:
        await callback.message.edit_text(
            text="Товар закончился", reply_markup=shop_menu_kb()
        )
    elif product.quantity >= 1 and balance >= callback_data.price:
        await ShopManager.update_products(callback_data.id)
        await ShopManager.update_balance(callback.from_user.id, callback_data.price)
        await ShopManager.add_history(
            user_id=callback.from_user.id,
            product_id=callback_data.id,
            price=callback_data.price,
            quantity=1,
        )
        await callback.message.edit_text(
            text=f"Поздравляю Вы купили 1 {callback_data.product}.Остаток обновлен.",
            reply_markup=shop_menu_kb(),
        )
    else:
        await callback.message.edit_text(
            text="недостаточно средств", reply_markup=shop_menu_kb()
        )
        return
