from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.callback_data import (
    BuyItemCallback,
    CheckTransaCallback,
)


def books_keyboard(items) -> InlineKeyboardMarkup:
    buttons = []
    for item in items:
        buttons.append(
            [
                InlineKeyboardButton(
                    text=item.title,
                    callback_data=BuyItemCallback(
                        action="view", item_id=item.id
                    ).pack(),
                )
            ]
        )
    buttons.append(
        [
            InlineKeyboardButton(
                text="🔙 Назад",
                callback_data=BuyItemCallback(item_id=0, action="back").pack(),
            )
        ]
    )
    return InlineKeyboardMarkup(inline_keyboard=buttons)

def buy_keyboard(item_id:int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Купить",
                    callback_data=BuyItemCallback(item_id=item_id,action='buy').pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Назад",
                    callback_data=BuyItemCallback(item_id=0,action="back").pack(),
                )
            ],
        ]
    )




def check_transa_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Я оплатил",
                    callback_data=CheckTransaCallback(action="buy").pack(),
                )
            ],
            [
                InlineKeyboardButton(
                    text="Передумал",
                    callback_data=CheckTransaCallback(action="cancel").pack(),
                )
            ],
        ]
    )
