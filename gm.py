import json
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# توکن ربات و شناسه چت ادمین
TELEGRAM_BOT_TOKEN = "8046438186:AAGjlj476vckhqfONymWaIQeqfpMEVkobac"
ADMIN_CHAT_ID = "5619969053"

# نام فایل JSON برای ذخیره کاربران
USERS_JSON_FILE = 'users.json'

# داده‌های کاربران
users_data = { "users": [] }

# بارگذاری اطلاعات از فایل JSON
def load_data_from_file():
    global users_data
    try:
        with open(USERS_JSON_FILE, 'r') as file:
            users_data = json.load(file)
    except Exception as e:
        print(f"Error reading users file: {e}")

# ذخیره اطلاعات به فایل JSON
def save_data_to_file():
    try:
        with open(USERS_JSON_FILE, 'w') as file:
            json.dump(users_data, file)
    except Exception as e:
        print(f"Error saving users data: {e}")

# ایجاد کاربر جدید
def create_user(chat_id):
    # بررسی اگر کاربر از قبل در سیستم موجود باشد
    user_exists = any(user['telegram_id'] == chat_id for user in users_data['users'])
    if user_exists:
        return

    # افزودن کاربر جدید
    users_data['users'].append({
        'telegram_id': chat_id,
        'balance': 0,
        'deposits': []
    })
    save_data_to_file()

# دریافت موجودی کاربر
def get_user_balance(chat_id):
    user = next((user for user in users_data['users'] if user['telegram_id'] == chat_id), None)
    return user['balance'] if user else 0

# ارسال دکمه‌های inline
def send_inline_buttons(update, buttons, message):
    reply_markup = InlineKeyboardMarkup(buttons)
    update.message.reply_text(message, reply_markup=reply_markup)

# شروع ربات و نمایش دکمه‌ها
def start(update, context):
    chat_id = update.message.chat.id
    create_user(chat_id)
    
    buttons = [
        [InlineKeyboardButton("موجودی", callback_data='balance')],
        [InlineKeyboardButton("شارژ حساب", callback_data='deposit')],
        [InlineKeyboardButton("راهنما", callback_data='help')]
    ]
    send_inline_buttons(update, buttons, "به ربات معاملات بیت‌کوین خوش آمدید! لطفاً یکی از گزینه‌ها را انتخاب کنید.")

# نمایش راهنما با دکمه‌ها
def help(update, context):
    buttons = [
        [InlineKeyboardButton("موجودی", callback_data='balance')],
        [InlineKeyboardButton("شارژ حساب", callback_data='deposit')]
    ]
    send_inline_buttons(update, buttons, "دستورات ربات:\n\n1. موجودی: مشاهده موجودی حساب.\n2. شارژ حساب: برای شارژ حساب.")
    
# موجودی کاربر
def balance(update, context):
    chat_id = update.message.chat.id
    balance = get_user_balance(chat_id)
    update.message.reply_text(f"💰 موجودی شما: {balance} USDT")

# شارژ حساب کاربر
def deposit(update, context):
    chat_id = update.message.chat.id
    update.message.reply_text("🔹 لطفاً مبلغ واریزی خود را به شماره کارت ارسال کنید.\n\n✅ سپس رسید واریز را ارسال کنید.")

# تایید واریز توسط ادمین
def accept_deposit(update, context):
    chat_id = update.message.chat.id
    
    # بررسی که ادمین باشد
    if chat_id != int(ADMIN_CHAT_ID):
        update.message.reply_text("❌ فقط ادمین می‌تواند این کار را انجام دهد.")
        return

    # بررسی اینکه پارامترهای صحیح ارسال شده باشند
    if len(context.args) < 2:
        update.message.reply_text("❌ لطفاً شماره چت کاربر و مبلغ واریزی را وارد کنید.\nبه این صورت: /accept [chat_id] [amount]")
        return

    user_chat_id = int(context.args[0])  # chat_id کاربر
    deposit_amount = float(context.args[1])  # مبلغ واریزی

    # پیدا کردن کاربر
    user = next((user for user in users_data['users'] if user['telegram_id'] == user_chat_id), None)
    if user:
        # افزودن مبلغ به موجودی کاربر
        user['balance'] += deposit_amount
        save_data_to_file()
        update.message.reply_text(f"✅ حساب کاربر با ID {user_chat_id} به مبلغ {deposit_amount} شارژ شد.")
    else:
        update.message.reply_text(f"❌ کاربری با ID {user_chat_id} پیدا نشد.")

# هندلر برای دکمه‌های inline
def button(update, context):
    query = update.callback_query
    query.answer()
    
    if query.data == 'balance':
        balance(update, context)
    elif query.data == 'deposit':
        deposit(update, context)
    elif query.data == 'help':
        help(update, context)

# بارگذاری داده‌ها از فایل JSON
load_data_from_file()

# راه‌اندازی ربات و افزودن هندلرها
updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("help", help))
dp.add_handler(CommandHandler("accept", accept_deposit))
dp.add_handler(MessageHandler(Filters.text & ~Filters.command, button))

# شروع ربات
updater.start_polling()
updater.idle()