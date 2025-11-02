import os
import telebot
from flask import Flask
from threading import Thread

# ======= تنظیمات از Environment Variables =======
TOKEN = os.environ.get("TOKEN")  # توکن بات
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # آیدی عددی خودت
PASSWORD = os.environ.get("PASSWORD", "1234")  # رمز پیش‌فرض
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/YourChannel")  # لینک کانال
# ================================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ------------------- ربات تلگرام -------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    # اطلاع دادن به ادمین که کسی بات رو استارت کرده
    bot.send_message(ADMIN_ID, f"{user_name} ({username}) بات را استارت کرد.")
    # پیام به کاربر
    bot.reply_to(message, "سلام! لطفا رمز را وارد کنید:")

@bot.message_handler(func=lambda message: True)
def check_password(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    if message.text == PASSWORD:
        bot.reply_to(message, f"رمز درست! این هم لینک کانال: {CHANNEL_LINK}")
        bot.send_message(ADMIN_ID, f"{user_name} ({username}) رمز را درست وارد کرد.")
    else:
        bot.reply_to(message, "رمز اشتباه است. دوباره امتحان کنید!")

def run_bot():
    print("🤖 Bot is running...")
    bot.infinity_polling(skip_pending=True)

# ------------------- وب سرور Flask -------------------
@app.route('/')
def home():
    return "✅ Telegram bot is running and healthy!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    print(f"🌐 Flask server listening on port {port}")
    app.run(host="0.0.0.0", port=port)

# ------------------- اجرای همزمان -------------------
if __name__ == "__main__":
    Thread(target=run_bot).start()
    Thread(target=run_flask).start()
