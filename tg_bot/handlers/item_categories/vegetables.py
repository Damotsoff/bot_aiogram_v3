from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.keyboards.callback_data import ShopMenuCallback
from tg_bot.keyboards.keyboard import vegetables_menu_kb
from tg_bot.services.shop_manager import ShopManager

router = Router()


@router.callback_query(
    ShopMenuCallback.filter((F.action == "list") & (F.category == "vegetables"))
)
async def show_vegetables(callback: CallbackQuery):
    vegetables = await ShopManager.get_vegetables()
    await callback.message.edit_text(
        "Овощи в наличии:", reply_markup=vegetables_menu_kb(products=vegetables)
    )
