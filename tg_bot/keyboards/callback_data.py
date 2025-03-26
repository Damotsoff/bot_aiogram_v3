# ✅ Новый способ (aiogram 3.x)
from aiogram.filters.callback_data import CallbackData

class BuyCallback(CallbackData, prefix="buy"):
    item_name: str
    quantity: int


# Для главного меню
class MainMenuCallback(CallbackData, prefix="main"):
    section: str  # "shop", "support", "profile"

# Для меню магазина
class ShopMenuCallback(CallbackData, prefix="shop"):
    category: str  # "fruits", "vegetables"
    action: str  # "list", "back"

# Для выбора товара
class ProductCallback(CallbackData, prefix="product"):
    item_id: int
    action: str  # "view", "buy"