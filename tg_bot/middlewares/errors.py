from aiogram import Router, F
from aiogram.types import Message, ErrorEvent
from aiogram.filters import ExceptionTypeFilter
import logging

error_router = Router()


@error_router.error(F.update.message.as_("message"), ExceptionTypeFilter(ValueError))
async def handle_error(error_event: ErrorEvent, message: Message):
    logging.error(error_event.exception, exc_info=True)
    await message.reply("Wrong value! Enter a number.")
