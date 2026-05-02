from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import os

BOT_TOKEN = os.getenv("8737222751:AAHKk9IjOyuOqa9H7MMoId5S8fjuwZUSQ9g")
BOT_USERNAME = "AdeElJuttDigitalS_Bot"

DATA_FILE = "data.json"

def load_data():
if os.path.exists(DATA_FILE):
try:
with open(DATA_FILE, "r") as f:
return json.load(f)
except:
return {}
return {}

def save_data(data):
with open(DATA_FILE, "w") as f:
json.dump(data, f)

data = load_data()

def get_user(user_id):
if user_id not in data:
data[user_id] = {
"balance": 0,
"referrals": 0,
"ref_by": None
}
return data[user_id]

def start(update, context):
user_id = str(update.effective_user.id)
user = get_user(user_id)

if context.args:
    ref = context.args[0]
    if ref != user_id:
        ref_user = get_user(ref)
        if user["ref_by"] is None:
            user["ref_by"] = ref
            ref_user["balance"] += 20
            ref_user["referrals"] += 1
            save_data(data)

keyboard = [
    [InlineKeyboardButton("🛒 Services", callback_data="services")],
    [InlineKeyboardButton("👥 Referral", callback_data="referral")],
    [InlineKeyboardButton("💰 Balance", callback_data="balance")],
    [InlineKeyboardButton("💵 Withdraw", callback_data="withdraw")],
    [InlineKeyboardButton("📱 WhatsApp", url="https://wa.me/923556023320")]
]

update.message.reply_text(
    "👋 Welcome to Adeel Jutt Bot",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

def buttons(update, context):
query = update.callback_query
user_id = str(query.from_user.id)
user = get_user(user_id)

query.answer()

if query.data == "services":
    text = "🛒 Services:\nTikTok UK - 600\nWeb Dev - 7000\nLogo - 300"

elif query.data == "referral":
    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    text = f"👥 Referral Link:\n{link}\nEarn Rs 20 per referral"

elif query.data == "balance":
    text = f"💰 Balance: {user['balance']}\n👥 Referrals: {user['referrals']}"

elif query.data == "withdraw":
    if user["balance"] >= 300:
        text = "💵 Eligible! Contact admin"
    else:
        text = "❌ Minimum withdraw Rs 300"

query.edit_message_text(text)

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CallbackQueryHandler(buttons))

updater.start_polling()
updater.idle()
