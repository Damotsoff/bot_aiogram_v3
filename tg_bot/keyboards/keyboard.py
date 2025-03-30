from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from tg_bot.keyboards.callback_data import (
    MainMenuCallback,
    ShopMenuCallback,
    ProductCallback,
    ViewProfileCallback,
    SupportCallback,
)

bank = {"balance": 10000}

product_storage = {
    "vegetables": {
        "🍅Помидоры": {
            "id": 1,
            "quantity": 10,
            "price": 234,
        },
        "🥦Брокколи": {
            "id": 2,
            "quantity": 5,
            "price": 454,
        },
    },
    "fruits": {
        "Яблоки": {"id": 4, "quantity": 5, "price": 324.0},
        "Груши": {"id": 5, "quantity": 6, "price": 548},
    },
}


# Главное меню
def main_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🛒 Магазин",
                    callback_data=MainMenuCallback(section="shop", action="").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🆘 Поддержка",
                    callback_data=MainMenuCallback(section="support", action="").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="👤 Профиль",
                    callback_data=MainMenuCallback(section="profile", action="").pack(),
                )
            ],
        ]
    )


# Меню магазина
def shop_menu_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🍎 Фрукты",
                    callback_data=ShopMenuCallback(
                        category="fruits", action="list"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🥦 Овощи",
                    callback_data=ShopMenuCallback(
                        category="vegetables", action="list"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Главное меню",
                    callback_data=MainMenuCallback(section="", action="back").pack(),
                )
            ],
        ]
    )


# Меню товаров (фрукты)
def fruits_menu_kb():
    apple = product_storage["fruits"]["Яблоки"]
    pears = product_storage["fruits"]["Груши"]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Яблоки (осталось {apple["quantity"]})",
                    callback_data=ProductCallback(
                        item_id=apple["id"],
                        quantity=apple["quantity"],
                        action="view",
                        category="fruits",
                        product="Яблоки",
                        price=apple["price"],
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"Груши ((осталось {pears["quantity"]}))",
                    callback_data=ProductCallback(
                        item_id=2,
                        action="view",
                        category="fruits",
                        product="Груши",
                        price=pears["price"],
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=ShopMenuCallback(
                        category="fruits", action="back"
                    ).pack(),
                )
            ],
        ]
    )


def vegetables_menu_kb():
    tomato = product_storage["vegetables"]["🍅Помидоры"]
    broccoli = product_storage["vegetables"]["🥦Брокколи"]
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🍅 Помидоры (осталось {tomato["quantity"]} штук)",
                    callback_data=ProductCallback(
                        item_id=tomato["id"],
                        action="view",
                        category="vegetables",
                        product="🍅Помидоры",
                        quantity=tomato["quantity"],
                        price=tomato["price"],
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text=f"🥦Брокколи (осталось {broccoli["quantity"]} штук)",
                    callback_data=ProductCallback(
                        item_id=broccoli["id"],
                        action="view",
                        category="vegetables",
                        product="🥦Брокколи",
                        quantity=broccoli["quantity"],
                        price=broccoli["price"],
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=ShopMenuCallback(
                        category="vegetables", action="back"
                    ).pack(),
                )
            ],
        ]
    )


def profile_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💲 Посмотреть баланс",
                    callback_data=ViewProfileCallback(
                        balance=bank["balance"], action="view"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Главное меню",
                    callback_data=MainMenuCallback(section="", action="back").pack(),
                )
            ],
        ]
    )


def support_kb(user_id: int | None = None):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Создать обращение",
                    callback_data=SupportCallback(
                        action="create_ticket",
                        user_id=user_id,  # Передаём user_id, если он известен
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Главное меню",
                    callback_data=MainMenuCallback(section="", action="back").pack(),
                )
            ],
        ]
    )


def purchased_kb(callback_data):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=ProductCallback(
                        item_id=callback_data.item_id,
                        action="buy",
                        category=callback_data.category,
                        product=callback_data.product,
                        price=callback_data.price,
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=ShopMenuCallback(
                        category=callback_data.category, action="list"
                    ).pack(),
                )
            ],
        ]
    )
