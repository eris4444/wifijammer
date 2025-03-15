from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import json

# توکن ربات و شناسه ادمین
TELEGRAM_BOT_TOKEN = "8046438186:AAGjlj476vckhqfONymWaIQeqfpMEVkobac"
ADMIN_CHAT_ID = "5619969053"

# ساختار داده کاربران
users_data = { "users": [] }

# فایل JSON ذخیره‌سازی
USERS_JSON_FILE = "users.json"

# فراخوانی webhook تلگرام
async def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    text = update.message.text.strip()

    # ورود و ثبت کاربر جدید
    if text == "/start":
        create_user(chat_id)
        await update.message.reply_text("به ربات معاملات بیت‌کوین خوش آمدید! از /help برای راهنما استفاده کنید.")

async def help(update: Update, context: CallbackContext):
    await update.message.reply_text("دستورات ربات:\n/balance - مشاهده موجودی\n/deposit - شارژ حساب\n/trade - انجام معامله")

async def balance(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    balance = get_user_balance(chat_id)
    await update.message.reply_text(f"💰 موجودی شما: {balance} USDT")

async def deposit(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    await update.message.reply_text("🔹 لطفاً مبلغ واریزی خود را به شماره کارت زیر ارسال کنید:\n\n💳 1234-5678-9012-3456\n\n✅ سپس رسید واریز را ارسال کنید.")

async def trade(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id
    if len(context.args) != 2:
        await update.message.reply_text("❌ دستور نامعتبر است. لطفاً از فرمت صحیح استفاده کنید: /trade amount leverage")
        return
    amount = float(context.args[0])
    leverage = int(context.args[1])
    await handle_trade(chat_id, amount, leverage)

async def handle_trade(chat_id, amount, leverage):
    if amount <= 0 or leverage <= 0 or leverage > 10:
        return await send_telegram_message(chat_id, "❌ مقدار معامله یا ضریب نامعتبر است.")

    balance = get_user_balance(chat_id)
    if amount > balance:
        return await send_telegram_message(chat_id, "❌ موجودی شما کافی نیست.")

    new_balance = balance - amount
    user = get_user(chat_id)
    if user:
        user["balance"] = new_balance

    save_data_to_file()

    return await send_telegram_message(chat_id, f"✅ معامله به ارزش {amount} USDT با ضریب {leverage} انجام شد.")

def get_user(chat_id):
    return next((user for user in users_data["users"] if user["telegram_id"] == chat_id), None)

def get_user_balance(chat_id):
    user = get_user(chat_id)
    return user["balance"] if user else 0

def create_user(chat_id):
    if get_user(chat_id):
        return

    users_data["users"].append({
        "telegram_id": chat_id,
        "balance": 0,
        "deposits": []
    })

    save_data_to_file()

def save_data_to_file():
    with open(USERS_JSON_FILE, "w") as f:
        json.dump(users_data, f)

async def send_telegram_message(chat_id, text):
    return await context.bot.send_message(chat_id=chat_id, text=text)

# در اینجا باید webhook ربات را ثبت کنید (اختیاری)
# پس از این که webhook تنظیم شد، این بخش فعال می‌شود.

async def main():
    # ایجاد application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # افزودن handler ها
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("balance", balance))
    application.add_handler(CommandHandler("deposit", deposit))
    application.add_handler(CommandHandler("trade", trade, filters=args))

    # شروع ربات
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())