from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.keyboards.callback_data import ShopMenuCallback, ProductCallback
from tg_bot.keyboards.keyboard import fruits_menu_kb
from tg_bot.services.shop_manager import ShopManager

router = Router()


@router.callback_query(
    ShopMenuCallback.filter((F.action == "list") & (F.category == "beer"))
)
async def show_fruits(callback: CallbackQuery):
    beer = await ShopManager.get_beer()
    await callback.message.edit_text(
        "В наличии:",
        reply_markup=fruits_menu_kb(products=beer),
    )
