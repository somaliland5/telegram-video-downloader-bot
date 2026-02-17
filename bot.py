import os
import requests
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

TOKEN = os.getenv("BOT_TOKEN")
BACKEND = os.getenv("BACKEND_URL")

if not TOKEN or not BACKEND:
    raise ValueError("BOT_TOKEN and BACKEND_URL must be set in Environment Variables")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")


# ===== START COMMAND =====
@bot.message_handler(commands=["start"])
def start(message):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton(
            "🌐 Open Downloader Web",
            web_app=WebAppInfo(f"{BACKEND}/web")
        )
    )
    bot.send_message(
        message.chat.id,
        "🎬 Welcome! Send TikTok or Instagram link here to download videos.",
        reply_markup=kb
    )


# ===== LINK HANDLER =====
@bot.message_handler(func=lambda m: "http" in m.text)
def handle_link(message):
    url = message.text.strip()
    bot.send_message(message.chat.id, "⏳ Downloading...")

    try:
        res = requests.post(f"{BACKEND}/download", json={"user": message.from_user.id, "url": url}, timeout=60)
        data = res.json()
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error connecting to backend: {e}")
        return

    if data.get("video"):
        bot.send_video(message.chat.id, data["video"])
    else:
        bot.send_message(message.chat.id, "❌ Failed to download. Check your link or try again.")


# ===== RUN BOT =====
print("🤖 Telegram Bot is running...")
bot.infinity_polling(skip_pending=True)
