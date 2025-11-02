import os
import telebot

# ======= تنظیمات از Environment Variables =======
TOKEN = os.environ.get("TOKEN")  # توکن بات
ADMIN_ID = int(os.environ.get("ADMIN_ID"))  # آیدی عددی خودت
PASSWORD = os.environ.get("PASSWORD", "1234")  # رمز پیش‌فرض "1234"
CHANNEL_LINK = os.environ.get("CHANNEL_LINK", "https://t.me/YourChannel")  # لینک کانال
# ================================================

bot = telebot.TeleBot(TOKEN)

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
        # اطلاع دادن به ادمین که رمز درست وارد شده
        bot.send_message(ADMIN_ID, f"{user_name} ({username}) رمز را درست وارد کرد.")
    else:
        bot.reply_to(message, "رمز اشتباه است. دوباره امتحان کنید!")

bot.infinity_polling()
