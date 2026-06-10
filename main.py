import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage

from database import create_tables, insert_user
from buttons.inline_butto import start_inline_buttons, operator_inline_buttons
from menu import router as menu_router
from operators.maxsulot import product_router

API_TOKEN = "8660554360:AAGcE_SAfsU8rUdbH4IjzH1VxspzYqWyaLw"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

OPERATORS_id = [8327989068]


@dp.message(CommandStart())
async def start_command(message: types.Message):
    created_at_str = message.date.strftime("%Y-%m-%d %H:%M:%S")
    insert_user(
        chat_id=message.chat.id,
        first_name=message.from_user.first_name,
        username=message.from_user.username,
        language_code=message.from_user.language_code,
        is_bot=message.from_user.is_bot,
        created_at=created_at_str,
    )

    if message.from_user.id in OPERATORS_id:
        operator_matn = (
            f"Salom, Operator {message.from_user.first_name}! 🛠\n\n"
            f"Siz tizimda operator sifatida ro'yxatdan o'tgansiz.\n"
            f"Kelayotgan buyurtmalarni boshqarish va mahsulotlar menyusini "
            f"tahrirlash uchun pastdagi panelga kiring. 👇"
        )
        await message.answer(
            text=operator_matn,
            reply_markup=operator_inline_buttons()
        )
    else:
        mijoz_matn = (
            f"Assalomu alaykum, {message.from_user.first_name}! 👋\n\n"
            f"United Burger do'konidan buyurtma berish botiga xush kelibsiz! "
            f"Och qoldingizmi? Unda darhol menyu bilan tanishing! 👇\n\n"
            f"🕒 Ish vaqtimiz: 10:00 dan 03:00 gacha\n"
            f"📍 Manzil: Toshkent shahar (yetkazib berish xizmati mavjud)"
        )
        await message.answer(
            text=mijoz_matn,
            reply_markup=start_inline_buttons()
        )


async def main():
    create_tables()   # ← bitta funksiya, hammasi shu yerda
    dp.include_router(menu_router)
    dp.include_router(product_router)
    logging.basicConfig(level=logging.INFO)
    print("✅ Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())