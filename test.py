import logging
import io
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from blockcypher import generate_new_address, get_address_overview


import qrcode
import asyncio
from tg_bot.config import load_config

# from aiogram import executor

# Настройки логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка конфигурации
config = load_config()
TELEGRAM_API_TOKEN = config.tg_bot.token
BLOCKCYPHER_API_TOKEN = config.tg_bot.blockcypher
CRYPTO_COIN = "btc-testnet"

# Инициализация бота

router = Router()
# dp.include_router(router)

# Хранилище активных платежей
active_payments = {}


class PaymentState(StatesGroup):
    waiting_for_payment = State()


# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    start_text = (
        "🚀 Добро пожаловать в Crypto Payment Bot!\n"
        "Я помогу вам принимать тестовые платежи в Bitcoin testnet\n"
        "Используйте команду /pay чтобы создать платежный адрес"
    )
    await message.answer(start_text)


# Обработчик команды /pay
@router.message(Command("pay"))
async def cmd_pay(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    amount = 0.00001  # Сумма в BTC testnet

    try:
        # Генерация нового адреса
        address_data = generate_new_address(
            coin_symbol="btc-testnet",
            api_key=BLOCKCYPHER_API_TOKEN,
            # address_type="p2pkh",  # Явно указываем тип адреса
        )
        # address = address_data["address"]
        address="mnwh9sDLdUZM8QwTBWCtZKGczXZPGP4QPq"

        # Сохранение состояния
        await state.update_data(address=address, amount=amount)
        active_payments[user_id] = {
            "address": address,
            "amount": amount,
            "status": "pending",
        }

        # Генерация QR-кода
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(address)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        # Подготовка изображения для отправки
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format="PNG")
        img_byte_arr.seek(0)

        # Формирование сообщения
        message_text = (
            f"💸 Тестовый платеж на сумму: {amount} BTC (testnet)\n\n"
            f"🔗 Адрес: `{address}`\n"
            f"📊 Проверить баланс: [Blockchair](https://blockchair.com/bitcoin/testnet/address/{address})"
        )

        # Отправка информации пользователю
        await message.answer(
            text=message_text, parse_mode="Markdown", disable_web_page_preview=True
        )
        await message.answer_photo(
            photo=types.BufferedInputFile(
                img_byte_arr.getvalue(), filename="payment_qr.png"
            ),
            caption="📲 Отсканируйте QR-код для оплаты",
        )

        # Запуск проверки платежа
        asyncio.create_task(check_payment(user_id, address, amount))

    except Exception as e:
        logger.error(f"Error generating address: {e}")
        await message.answer(
            "⚠️ Произошла ошибка при создании адреса. Попробуйте позже."
        )


# Функция проверки платежа
from blockcypher import get_address_overview, get_address_details  # Правильные методы

async def check_payment(user_id: int, address: str, required_amount: float):
    payment_detected = False
    check_count = 0
    
    while check_count < 30:  # Максимум 30 проверок (~15 минут)
        try:
            # 1. Проверка неподтвержденных транзакций
            unconfirmed = get_address_details(
                address=address,
                coin_symbol=CRYPTO_COIN,
                api_key=BLOCKCYPHER_API_TOKEN
            )
            print(unconfirmed)
            if unconfirmed['unconfirmed_txrefs']:
                total_unconfirmed = sum(
                    [tx['total'] for tx in unconfirmed['unconfirmed_txrefs']]
                ) / 1e8
                
                if not payment_detected:
                    await bot.send_message(
                        user_id, 
                        f"🕒 Обнаружена неподтвержденная транзакция на {total_unconfirmed} BTC!"
                    )
                    payment_detected = True

            # 2. Проверка подтвержденного баланса
            confirmed_data = get_address_overview(
                address=address,
                coin_symbol=CRYPTO_COIN,
                api_key=BLOCKCYPHER_API_TOKEN
            )
            confirmed = confirmed_data['balance'] / 1e8
            
            if confirmed >= required_amount:
                await bot.send_message(user_id, "✅ Платеж подтвержден в блокчейне!")
                active_payments.pop(user_id, None)
                return
                
            # 3. Управление задержками
            await asyncio.sleep(20 if payment_detected else 30)
            check_count += 1

        except Exception as e:
            # raise
            logger.error(f"Payment check error: {e}")
            await asyncio.sleep(60)
    
    await bot.send_message(user_id, "⚠️ Платеж не подтвержден. Используйте /pay для нового адреса.")

async def main():
    bot = Bot(token=TELEGRAM_API_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)
    await dp.start_polling(bot, skip_updates=True)
    await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main=main())
