import telebot
from telebot import types
from flask import Flask
from threading import Thread
import time

TOKEN = "ТВОЙ_ТОКЕН"

bot = telebot.TeleBot(TOKEN)

# ссылка на файл
FILE_LINK = "https://t.me/твоя_ссылка"

# тексты рассылки
MESSAGES = {
    1: "",
    2: "",
    3: "Текст 3 дня",
    4: "Текст 4 дня",
    5: "Текст 5 дня",
    6: "Текст 6 дня",
    7: "Текст 7 дня",
    8: "Текст 8 дня",
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
        "Добро пожаловать",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "НЕЖНОСТЬ")
def tenderness(message):
    text = "ТВОЙ ТЕКСТ"

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
