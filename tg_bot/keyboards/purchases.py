from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from tg_bot.keyboards.callback_data import (
    BuyItemCallback,
    CheckTransaCallback,
    MainMenuCallback,
)


def buy_keyboard(item_id: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="купить",
                    callback_data=BuyItemCallback(item_id=item_id, action="buy").pack(),
                )
            ]
        ]
    )


def back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="назад",
                    callback_data=MainMenuCallback(section="shop", action="").pack(),
                )
            ]
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
