import os
import telebot
from flask import Flask, request

# ======= تنظیمات از Environment Variables =======
TOKEN = os.environ.get("TOKEN")  # توکن بات
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # آیدی عددی ادمین
PASSWORD = os.environ.get("PASSWORD", "1234")  # رمز پیش‌فرض
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/YourChannel")  # لینک کانال
# ================================================

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ------------------- هندلرهای ربات -------------------
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    # اطلاع دادن به ادمین که کسی بات را استارت کرده
    bot.send_message(ADMIN_ID, f"{user_name} (@{username}) بات را استارت کرد.")
    bot.reply_to(message, "سلام! لطفا رمز را وارد کنید:")

@bot.message_handler(func=lambda message: True)
def check_password(message):
    user_name = message.from_user.first_name
    username = message.from_user.username
    if message.text == PASSWORD:
        bot.reply_to(message, f"رمز درست ✅ این هم لینک کانال:\n{CHANNEL_LINK}")
        bot.send_message(ADMIN_ID, f"{user_name} (@{username}) رمز را درست وارد کرد.")
    else:
        bot.reply_to(message, "❌ رمز اشتباه است. دوباره امتحان کنید!")

# ------------------- مسیرهای Flask -------------------
@app.route('/')
def home():
    return "✅ Telegram bot is running via webhook!"

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.data.decode('utf-8'))
    bot.process_new_updates([update])
    return "OK", 200

# ------------------- اجرای وب‌هوک -------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    webhook_url = f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"

    # حذف هر وب‌هوک قبلی و تنظیم جدید
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

    print(f"🌐 Webhook set to: {webhook_url}")
    app.run(host="0.0.0.0", port=port)
