import os
import telebot
import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN")
BACKEND = os.getenv("BACKEND_URL")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(m):

    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(
            "🌐 Open Downloader Web",
            web_app=WebAppInfo(f"{BACKEND}/web")
        )
    )

    bot.send_message(
        m.chat.id,
        "🎬 Send TikTok or Instagram link to download",
        reply_markup=kb
    )


@bot.message_handler(func=lambda m: "http" in m.text)
def download(message):

    bot.send_message(message.chat.id, "⏳ Downloading...")

    r = requests.post(
        f"{BACKEND}/download",
        json={
            "user": message.from_user.id,
            "url": message.text
        }
    ).json()

    if r.get("video"):
        bot.send_video(message.chat.id, r["video"])
    else:
        bot.send_message(message.chat.id, "❌ Failed")


bot.infinity_polling()
