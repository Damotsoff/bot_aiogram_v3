from aiogram.filters.callback_data import CallbackData


# Для главного меню
class MainMenuCallback(CallbackData, prefix="main"):
    section: str  # "shop", "support", "profile"
    action: str


class ViewProfileCallback(CallbackData, prefix="profile"):
    balance: int
    action: str = ""


class SupportCallback(CallbackData, prefix="support"):
    action: str  # "create_ticket" или другие действия
    user_id: int | None = None  # Опционально, можно передать сразу


# Для меню магазина
class ShopMenuCallback(CallbackData, prefix="shop"):
    category: str  # "fruits", "vegetables"
    action: str  # "list", "back"


# Для выбора товара
class ProductCallback(CallbackData, prefix="product"):
    item_id: int
    product: str
    action: str  # "view", "buy"
    category: str
    quantity: int = 1
    price: float
