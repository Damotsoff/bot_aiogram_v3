from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from tg_bot.states.states import SupportStates
from tg_bot.keyboards.keyboard import support_kb
from tg_bot.keyboards.callback_data import MainMenuCallback, SupportCallback
from tg_bot.services.shop_manager import ShopManager


router = Router()


@router.callback_query(MainMenuCallback.filter(F.section == "support"))
async def support(callback: CallbackQuery):

    await callback.message.edit_text(
        "Support", reply_markup=support_kb(callback.from_user.id)
    )


@router.message(SupportStates.waiting_for_support_text)
async def process_support_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    support_text = message.text
    full_name = message.from_user.full_name
    await ShopManager.add_ticket(
        user_id=user_id, text=support_text, full_name=full_name
    )

    await message.answer(
        text="🆘 Новое обращение:\n"
        f"👤 User ID: {user_id}\n"
        f"📄 Текст: {support_text}",
    )

    await message.answer(
        "✅ Ваше обращение отправлено! Спасибо.",
        reply_markup=support_kb(user_id),
    )

    await state.clear()


@router.callback_query(SupportCallback.filter(F.action == "create_ticket"))
async def handle_support_request(
    callback: CallbackQuery,
    state: FSMContext,
):
    await callback.message.answer(text="📝 Опишите вашу проблему:", reply_markup=None)
    await state.set_state(SupportStates.waiting_for_support_text)
    await callback.answer()
