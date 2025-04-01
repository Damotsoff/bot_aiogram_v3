from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from tg_bot.keyboards.keyboard import support_kb
from tg_bot.keyboards.callback_data import MainMenuCallback, SupportCallback


router = Router()


class SupportStates(StatesGroup):
    waiting_for_support_text = State()


@router.callback_query(MainMenuCallback.filter(F.section == "support"))
async def support(callback: CallbackQuery):

    await callback.message.edit_text(
        "Support", reply_markup=support_kb(callback.from_user.id)
    )


@router.message(SupportStates.waiting_for_support_text)
async def process_support_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    support_text = message.text

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

    # Подтверждаем обработку callback (убираем "часики" на кнопке)
    await callback.answer()
