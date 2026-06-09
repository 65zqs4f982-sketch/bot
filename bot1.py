import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

TOKEN = "8637657636:AAG7PYR6W2jWEeIrUhGggouj-u7niuWiaWg"

bot = telebot.TeleBot(TOKEN)

# ссылка на файл
FILE_LINK = "https://t.me/c/3863601162/7"

# тексты рассылки
MESSAGES = {
        "✨День 1: Просто спроси себя сегодня «Чего я хочу прямо сейчас?» Не «что надо», а что хочется тебе",
        "🕯️День 2: Зажги свечу сегодня вечером. Посиди в тишине 5 минут. Просто побудь с собой.",
        "📝День 3: Напиши 3 вещи, за которые ты благодарна себе сегодня. Даже маленькие.",
        "🚶🏼‍♀️День 4: Выйди на 15-минутную прогулку без телефона. Посмотри по сторонам.",
        "💧День 5: Выпей стакан воды медленно, с благодарностью. Скажи себе: «Я забочусь о тебе».",
        "🎵День 6: Включи песню, которая тебя вдохновляла в юности. Потанцуй.",
        "🌸День 7: Посмотри в зеркало и скажи: «Я ценна. Просто потому что я есть».",
        "🎁Бонус: Ты прошла первую неделю! Вот тебе дополнительная идея: купи себе цветы без повода.",
}

users = {}

# кнопка
markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn = types.KeyboardButton("НЕЖНОСТЬ")
markup.add(btn)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id

    if user_id not in users:
        users[user_id] = 1

    bot.send_message(
        user_id,
        "Привет♥️ нажми на кнопку НЕЖНОСТЬ, чтобы получить файл с 50 идеями для себя",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "НЕЖНОСТЬ")
def tenderness(message):
    text = "🌸Вы получили файл и теперь будете получать ежедневную рассылку с идеями для улчушения себя🌸"

    bot.send_message(message.chat.id, text)
    bot.send_message(message.chat.id, FILE_LINK)

# рассылка
def mailing():
    while True:
        for user_id in list(users.keys()):
            day = users[user_id]

            if day <= 8:
                try:
                    bot.send_message(user_id, MESSAGES[day])
                    users[user_id] += 1
                except:
                    pass

        time.sleep(86400)

# веб сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running"

def run():
    app.run(host="0.0.0.0", port=10000)

Thread(target=mailing).start()
Thread(target=run).start()

bot.infinity_polling()
