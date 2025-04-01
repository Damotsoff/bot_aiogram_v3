from aiogram.filters.callback_data import CallbackData


# Для главного меню
class MainMenuCallback(CallbackData, prefix="main"):
    section: str  # "shop", "support", "profile"
    action: str


class ShopMenuCallback(CallbackData, prefix="shop"):
    category: str  # "fruits", "vegetables"
    action: str  # "list", "back"


class ProductCallback(CallbackData, prefix="product"):
    id: int
    product: str
    action: str  # "view", "buy"
    category: str
    quantity: int = 1
    price: float


class ViewProfileCallback(CallbackData, prefix="profile"):
    balance: int
    action: str = ""


class SupportCallback(CallbackData, prefix="support"):
    action: str  # "create_ticket" или другие действия
    id: int | None = None  # Опционально, можно передать сразу
