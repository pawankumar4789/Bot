import os
import random
import string
import requests
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY")
ADMIN_ID = int(os.environ.get("5470646229"))  # Add your Telegram ID in Render secret
API_KEY = os.environ.get("ie5pd3acp7iruk9eowlnxxambo42cwr2")     # Your SMM Panel API Key
API_URL = os.environ.get("https://easysmmpanel.com/order/6104546")     # Your Panel API URL

service_id_map = {
    'likes': 101,
    'views': 102,
    'comments': 103
}

user_data = {}

def generate_key(length=10):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def place_order(service, link, quantity):
    response = requests.post(API_URL, data={
        "key": API_KEY,
        "action": "add",
        "service": service_id_map[service],
        "link": link,
        "quantity": quantity
    })
    return response.json()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💖 Likes", callback_data='likes')],
        [InlineKeyboardButton("👁‍🗨 Views", callback_data='views')],
        [InlineKeyboardButton("🗨️ Comments", callback_data='comments')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🙏 Welcome to VIP Instagram Panel!\nSelect a service to continue:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_data[query.from_user.id] = {'service': query.data}
    await query.edit_message_text("📎 Send your Instagram post link:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text

    if text.lower() == "done":
        key = generate_key()
        await update.message.reply_text(f"✅ Payment verified!\n🎁 Your key: `{key}`", parse_mode='Markdown')
        return

    if user_id in user_data and 'service' in user_data[user_id] and 'link' not in user_data[user_id]:
        user_data[user_id]['link'] = text
        await update.message.reply_text("🔢 Now enter quantity:")
    elif user_id in user_data and 'link' in user_data[user_id]:
        try:
            quantity = int(text)
            user_data[user_id]['quantity'] = quantity
            service = user_data[user_id]['service']
            link = user_data[user_id]['link']
            price = quantity * 0.10

            await update.message.reply_text(
                f"🛒 Order Details:\nService: {service}\nLink: {link}\nQuantity: {quantity}\n💰 Price: ₹{price:.2f}\n"
                "Send payment to this UPI:\n📲 `pawankumar72010@fam`\n\nThen type *done*.",
                parse_mode='Markdown'
            )

            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📥 New Order:\nService: {service}\nLink: {link}\nQty: {quantity}\nUser ID: {user_id}"
            )

            # Uncomment to place real order
            # result = place_order(service, link, quantity)
            # await update.message.reply_text(f"🛠 Order Placed: {result}")

        except ValueError:
            await update.message.reply_text("❌ Please enter a valid number.")
    else:
        await update.message.reply_text("🚀 Please type /start to begin.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📘 Type /start to place an order.\n💸 Pay to UPI above and reply 'done'.")

# Flask server to support webhook
app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    application.update_queue.put(update)
    return "ok"

if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        url_path=BOT_TOKEN,
        webhook_url=f"https://your-render-url.onrender.com/{BOT_TOKEN}"
    )
