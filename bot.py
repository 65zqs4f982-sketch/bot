import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.executor import start_webhook
import aiosqlite

API_TOKEN = os.getenv("8637657636:AAG7PYR6W2jWEeIrUhGggouj-u7niuWiaWg")

# --- ВАЖНО: сюда вставишь ссылку Render ---
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")  
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = "0.0.0.0"
WEBAPP_PORT = int(os.getenv("PORT", 10000))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# --- ССЫЛКА НА ФАЙЛ ---
FILE_LINK = "https://t.me/c/3863601162/7"

# --- КНОПКА ---
main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
main_kb.add(KeyboardButton("НЕЖНОСТЬ"))

# --- БАЗА ---
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

    await msg.answer("Привет♥️, нажми на кнопку НЕЖНОСТЬ и получи свой файл с 50 идеями", reply_markup=main_kb)

# --- НЕЖНОСТЬ ---
@dp.message_handler(lambda m: m.text == "НЕЖНОСТЬ")
async def tenderness(msg: types.Message):
    kb = InlineKeyboardMarkup()
    kb.add(InlineKeyboardButton("📎 Открыть файл", url=FILE_LINK))

    await msg.answer("Ты получил файл, перейди по ссылке чтобы его забрать, а также ты будешь получать каждый день сообщение с напоминанием💖", reply_markup=kb)

# --- РАССЫЛКА ---
async def mailing():
    texts = [
        "✨День 1: Просто спроси себя сегодня «Чего я хочу прямо сейчас?» Не «что надо», а что хочется тебе",
        "🕯️День 2: Зажги свечу сегодня вечером. Посиди в тишине 5 минут. Просто побудь с собой.",
        "📝День 3: Напиши 3 вещи, за которые ты благодарна себе сегодня. Даже маленькие.",
        "🚶🏼‍♀️День 4: Выйди на 15-минутную прогулку без телефона. Посмотри по сторонам.",
        "💧День 5: Выпей стакан воды медленно, с благодарностью. Скажи себе: «Я забочусь о тебе».",
        "🎵День 6: Включи песню, которая тебя вдохновляла в юности. Потанцуй ",
        "♥️День 7: Посмотри в зеркало и скажи: «Я ценна. Просто потому что я есть».",
        "🎁Бонус: Ты прошла первую неделю! Вот тебе дополнительная идея: купи себе цветы без повода. ",
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

                        await bot.send_message(user_id, texts[day], reply_markup=kb)

                        await db.execute(
                            "UPDATE users SET day = ? WHERE user_id = ?",
                            (day + 1, user_id)
                        )
                    except:
                        pass

            await db.commit()

        await asyncio.sleep(86400)

# --- СТАРТ WEBHOOK ---
async def on_startup(dp):
    await init_db()
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(mailing())

async def on_shutdown(dp):
    await bot.delete_webhook()

if __name__ == "__main__":
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
