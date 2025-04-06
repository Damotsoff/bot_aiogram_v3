from aiogram import Router, F
from aiogram.types import CallbackQuery
from tg_bot.keyboards.callback_data import ShopMenuCallback, ProductCallback
from tg_bot.keyboards.keyboard import fruits_menu_kb
from tg_bot.services.shop_manager import ShopManager

router = Router()


@router.callback_query(
    ShopMenuCallback.filter((F.action == "list") & (F.category == "fruits"))
)
async def show_fruits(callback: CallbackQuery):
    fruits = await ShopManager.get_fruits()
    await callback.message.edit_text(
        "Фрукты в наличии:", reply_markup=fruits_menu_kb(products=fruits)
    )
