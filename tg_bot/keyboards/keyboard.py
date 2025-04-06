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
    CounterCallback,
    AdminCallback,
)


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
            [
                InlineKeyboardButton(
                    text=" Посчитайчик",
                    callback_data=MainMenuCallback(section="counter", action="").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text=" Администрирование",
                    callback_data=MainMenuCallback(section="admin", action="").pack(),
                )
            ],
        ]
    )


def admin_kb(**kwargs):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить товар",
                    callback_data=AdminCallback(action="view").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="удалить",
                    callback_data=AdminCallback(action="delete").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="назад",
                    callback_data=AdminCallback(action="back").pack(),
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
                    text="🍺 Пиво",
                    callback_data=ShopMenuCallback(
                        category="beer", action="list"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🍷 Вино",
                    callback_data=ShopMenuCallback(
                        category="wine", action="list"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="🥃 Крепкий алкоголь",
                    callback_data=ShopMenuCallback(
                        category="spirits", action="list"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="📕 Книги по программированию",
                    callback_data=ShopMenuCallback(
                        category="books", action="list"
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
def fruits_menu_kb(products) -> InlineKeyboardMarkup:
    """
    Генерирует клавиатуру с фруктами

    :param products: Список объектов Product
    :return: InlineKeyboardMarkup с кнопками товаров
    """
    buttons = []
    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{product.product} ({product.price} руб.) Осталось: {product.quantity}",
                    callback_data=ProductCallback(
                        action="view",
                        id=product.id,
                        category=product.category,
                        price=product.price,
                        product=product.product,
                    ).pack(),
                )
            ]
        )

    # Добавляем кнопку "Назад" если нужно
    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ShopMenuCallback(category="fruits", action="back").pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def vegetables_menu_kb(products) -> InlineKeyboardMarkup:
    buttons = []
    for product in products:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=f"{product.product} ({product.price} руб.) Осталось: {product.quantity}",
                    callback_data=ProductCallback(
                        action="view",
                        id=product.id,
                        category=product.category,
                        price=product.price,
                        product=product.product,
                    ).pack(),
                )
            ]
        )

    # Добавляем кнопку "Назад" если нужно
    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=ShopMenuCallback(
                    category="vegetables", action="back"
                ).pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def profile_kb(balance: int = 0):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💲 Посмотреть баланс",
                    callback_data=ViewProfileCallback(
                        balance=balance, action="view"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="💲 Пополнить баланс",
                    callback_data=ViewProfileCallback(
                        balance=0, action="balance"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Посмотреть историю покупок",
                    callback_data=ViewProfileCallback(
                        balance=0, action="history"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Выгрузить историю покупок в файл.",
                    callback_data=ViewProfileCallback(
                        balance=0, action="export_history"
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
                        id=user_id,  # Передаём user_id, если он известен
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


def counter_kb(user_id: int = 0, quantity: int = 0, item: str = "test"):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Добавить хрючево:)",
                    callback_data=CounterCallback(
                        id=user_id, quantity=quantity, item=item, action="create_count"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Вывести мое хрючево:)",
                    callback_data=CounterCallback(
                        id=user_id, quantity=quantity, item=item, action="view_count"
                    ).pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=CounterCallback(
                        id=user_id, quantity=quantity, item=item, action="back"
                    ).pack(),
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
                        id=callback_data.id,
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
