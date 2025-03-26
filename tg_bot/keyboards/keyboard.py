from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.callback_data import BuyCallback
from tg_bot.keyboards.callback_data import MainMenuCallback,ShopMenuCallback,ProductCallback


menu = ReplyKeyboardMarkup(
        keyboard=
        [
        [KeyboardButton(text="Котлетки")],
        [KeyboardButton(text="Макарошки"), KeyboardButton(text="Пюрешка")],
        ],
    resize_keyboard=True,
)



choise = InlineKeyboardMarkup(row_width=2,inline_keyboard=[
    [
        InlineKeyboardButton(text="Купить грушу",callback_data=BuyCallback(item_name="pear", quantity=2).pack()),
        InlineKeyboardButton(text="Купить яблоки",callback_data=BuyCallback(item_name="apple", quantity=1).pack()),
    ],
    [InlineKeyboardButton(text="Отмена",callback_data='cancel')],
])




# Главное меню
def main_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🛒 Магазин",
            callback_data=MainMenuCallback(section="shop").pack()
        )],
        [InlineKeyboardButton(
            text="🆘 Поддержка", 
            callback_data=MainMenuCallback(section="support").pack()
        )]
    ])

# Меню магазина
def shop_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🍎 Фрукты",
            callback_data=ShopMenuCallback(category="fruits", action="list").pack()
        )],
        [InlineKeyboardButton(
            text="🥦 Овощи",
            callback_data=ShopMenuCallback(category="vegetables", action="list").pack()
        )],
        [InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=ShopMenuCallback(category="", action="back").pack()
        )]
    ])

# Меню товаров (фрукты)
def fruits_menu_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Яблоки",
            callback_data=ProductCallback(item_id=1, action="view").pack()
        )],
        [InlineKeyboardButton(
            text="Груши",
            callback_data=ProductCallback(item_id=2, action="view").pack()
        )],
        [InlineKeyboardButton(
            text="🔙 Назад",
            callback_data=ShopMenuCallback(category="fruits", action="back").pack()
        )]
    ])