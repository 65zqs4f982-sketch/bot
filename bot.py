import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
import aiosqlite
from datetime import datetime

API_TOKEN = os.getenv("8637657636:AAG7PYR6W2jWEeIrUhGggouj-u7niuWiaWg")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ССЫЛКА НА ФАЙЛ ---
FILE_LINK = "https://t.me/c/3863601162/7"  # замени на свою ссылку

# --- КНОПКА В МЕНЮ ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("НЕЖНОСТЬ"))

# --- БАЗА ДАННЫХ ---
async def init_db():
    async with aiosqlite.connect("users.db") as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            day INTEGER DEFAULT 0
        )
        """)
        await db.commit()

# --- СТАРТ ---
@dp.message_handler(commands=["start"])
async def start(msg: types.Message):
    async with aiosqlite.connect("users.db") as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id, day) VALUES (?, ?)",
            (msg.from_user.id, 0)
        )
        await db.commit()

    await msg.answer("Привет ♥️, нажми на кнопку и я отправлю тебе файл с 50 идеями нежности✨", reply_markup=main_kb)

# --- КНОПКА НЕЖНОСТЬ ---
@dp.message_handler(lambda m: m.text == "НЕЖНОСТЬ")
async def tenderness(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📎 Открыть файл", url=FILE_LINK))

    await msg.answer("С этого дня ты будешь получать напоминания каждый день♥️", reply_markup=kb)

# --- РАССЫЛКА ---
async def mailing():
    texts = [
        "✨День 1: Просто спроси себя сегодня «Чего я хочу прямо сейчас?» Не «что надо», а что хочется тебе",
        "🕯️День 2: Зажги свечу сегодня вечером. Посиди в тишине 5 минут. Просто побудь с собой.",
        "📝День 3: Напиши 3 вещи, за которые ты благодарна себе сегодня. Даже маленькие.",
        "🚶🏼‍♀️День 4: Выйди на 15-минутную прогулку без телефона. Посмотри по сторонам.",
        "💧День 5: Выпей стакан воды медленно, с благодарностью. Скажи себе: «Я забочусь о тебе».",
        "🎵День 6: Включи песню, которая тебя вдохновляла в юности. Потанцуй",
        "🌸День 7: Посмотри в зеркало и скажи: «Я ценна. Просто потому что я есть».",
        "🎁День 8: Ты прошла первую неделю! Вот тебе дополнительная идея: купи себе цветы без повода.",
    ]

    while True:
        async with aiosqlite.connect("users.db") as db:
            users = await db.execute("SELECT user_id, day FROM users")
            users = await users.fetchall()

            for user_id, day in users:
                if day < len(texts):
                    try:
                        kb = InlineKeyboardMarkup()
                        kb.add(InlineKeyboardButton("📎 Открыть файл", url=FILE_LINK))

                        await bot.send_message(
                            user_id,
                            texts[day],
                            reply_markup=kb
                        )

                        await db.execute(
                            "UPDATE users SET day = ? WHERE user_id = ?",
                            (day + 1, user_id)
                        )
                    except:
                        pass

            await db.commit()

        await asyncio.sleep(86400)  # 1 день

# --- ЗАПУСК ---
async def on_startup(dp):
    await init_db()
    asyncio.create_task(mailing())

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
