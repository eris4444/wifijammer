import json
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import requests

# فعال کردن لاگ‌ها
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# توکن ربات تلگرام و ID ادمین
TELEGRAM_BOT_TOKEN = "8046438186:AAGjlj476vckhqfONymWaIQeqfpMEVkobac"
ADMIN_CHAT_ID = "5619969053"

# فایل JSON ذخیره‌سازی
USERS_JSON_FILE = "users.json"

# ساختار داده کاربران
users_data = {"users": []}

# تابع ارسال پیام تلگرام
def send_telegram_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    response = requests.post(url, json={'chat_id': chat_id, 'text': text})
    return response

# تابع ارسال عکس تلگرام
def send_telegram_photo(chat_id, file_id):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto'
    response = requests.post(url, json={'chat_id': chat_id, 'photo': file_id})
    return response

# تابع شروع (Start)
def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    create_user(chat_id)
    send_telegram_message(chat_id, "به ربات معاملات بیت‌کوین خوش آمدید! از /help برای راهنما استفاده کنید.")

# تابع راهنما (Help)
def help(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    send_telegram_message(chat_id, "دستورات ربات:\n/balance - مشاهده موجودی\n/deposit - شارژ حساب\n/trade - انجام معامله")

# تابع مشاهده موجودی (Balance)
def balance(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    balance = get_user_balance(chat_id)
    send_telegram_message(chat_id, f"💰 موجودی شما: {balance} USDT")

# تابع شارژ حساب (Deposit)
def deposit(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    send_telegram_message(chat_id, "🔹 لطفاً مبلغ واریزی خود را به شماره کارت زیر ارسال کنید:\n\n💳 1234-5678-9012-3456\n\n✅ سپس رسید واریز را ارسال کنید.")

# تابع پردازش رسید واریز
def handle_deposit_receipt(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        send_telegram_message(ADMIN_CHAT_ID, f"📩 رسید واریز جدید از کاربر {chat_id}:\n\n✔️ لطفاً بررسی کنید.")
        send_telegram_photo(ADMIN_CHAT_ID, file_id)
        send_telegram_message(chat_id, "✅ رسید شما دریافت شد و منتظر تایید ادمین است.")

# تابع انجام معامله (Trade)
def trade(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text.strip()
    try:
        _, amount, leverage = text.split(" ")
        amount = float(amount)
        leverage = int(leverage)
    except ValueError:
        send_telegram_message(chat_id, "❌ دستور معامله اشتباه است. فرمت صحیح: /trade <مقدار> <ضریب>")
        return

    if leverage <= 0 or leverage > 10:
        send_telegram_message(chat_id, "❌ ضریب معامله باید بین 1 تا 10 باشد.")
        return

    balance = get_user_balance(chat_id)
    if amount > balance:
        send_telegram_message(chat_id, "❌ موجودی شما کافی نیست.")
        return

    new_balance = balance - amount
    update_user_balance(chat_id, new_balance)

    send_telegram_message(chat_id, f"✅ معامله به ارزش {amount} USDT با ضریب {leverage} انجام شد.")

# ایجاد کاربر جدید
def create_user(chat_id):
    user_exists = any(user['telegram_id'] == chat_id for user in users_data['users'])
    if user_exists:
        return
    users_data['users'].append({
        "telegram_id": chat_id,
        "balance": 0,
        "deposits": []
    })
    save_data_to_file()

# دریافت موجودی کاربر
def get_user_balance(chat_id):
    user = next((user for user in users_data['users'] if user['telegram_id'] == chat_id), None)
    return user['balance'] if user else 0

# به روز رسانی موجودی کاربر
def update_user_balance(chat_id, new_balance):
    user = next((user for user in users_data['users'] if user['telegram_id'] == chat_id), None)
    if user:
        user['balance'] = new_balance
        save_data_to_file()

# ذخیره داده‌ها به فایل JSON
def save_data_to_file():
    with open(USERS_JSON_FILE, 'w') as f:
        json.dump(users_data, f)

# بارگذاری داده‌ها از فایل JSON
def load_data_from_file():
    global users_data
    try:
        with open(USERS_JSON_FILE, 'r') as f:
            users_data = json.load(f)
    except FileNotFoundError:
        users_data = {"users": []}

# تنظیم Webhook
def set_webhook():
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook?url=https://your-server-url.com/webhook'
    response = requests.get(url)
    if response.status_code == 200:
        print("Webhook با موفقیت تنظیم شد.")
    else:
        print("خطا در تنظیم Webhook.")

# پردازش Webhook
def webhook(update: Update, context: CallbackContext):
    if update.message:
        message = update.message.text.strip()
        chat_id = update.message.chat.id
        if message == "/start":
            start(update, context)
        elif message == "/help":
            help(update, context)
        elif message == "/balance":
            balance(update, context)
        elif message == "/deposit":
            deposit(update, context)
        elif message.startswith("/trade"):
            trade(update, context)
        else:
            send_telegram_message(chat_id, "❌ دستور نامعتبر است.")

# شروع ربات
def main():
    load_data_from_file()

    # استفاده از Webhook برای دریافت پیام‌ها
    set_webhook()

    # تنظیم آپدیت‌کننده و افزودن هندلرها
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("balance", balance))
    dp.add_handler(CommandHandler("deposit", deposit))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, webhook))
    dp.add_handler(MessageHandler(Filters.photo, handle_deposit_receipt))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()