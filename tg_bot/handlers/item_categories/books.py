from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.data.items import items
from tg_bot.keyboards.purchases import books_keyboard,buy_keyboard
from tg_bot.keyboards.keyboard import shop_menu_kb
from tg_bot.keyboards.callback_data import ShopMenuCallback, BuyItemCallback


router = Router()


@router.callback_query(
    ShopMenuCallback.filter((F.action == "list") & (F.category == "books"))
)
async def show_items(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Список литературы",
        reply_markup=books_keyboard(items=items),
    )


@router.callback_query(BuyItemCallback.filter(F.action == "back"))
async def back_to_shop(callback: CallbackQuery):
    try:
        await callback.message.delete()
        await callback.message.answer("Категории", reply_markup=shop_menu_kb())
    except Exception:
        new_message = await callback.message.answer(
            "Категории", reply_markup=shop_menu_kb()
        )
        if callback.message.message_id:
            await callback.message.delete()
    await callback.answer()


@router.callback_query(BuyItemCallback.filter(F.action == "view"))
async def view_item(callback: CallbackQuery, callback_data: BuyItemCallback):
    item_id = callback_data.item_id - 1
    caption = """
Название продукта : {title}
<i>Описание:</i>
{description}
<u>Цена</u> {price:.2f} <b>RUB</b>
            """
    
    await callback.message.answer_photo(
        photo=items[item_id].photo,
        caption=caption.format(
            title=items[item_id].title,
            description=items[item_id].description,
            price=items[item_id].price,
        ),
        parse_mode="HTML",
        reply_markup=buy_keyboard(item_id=item_id),
    )
