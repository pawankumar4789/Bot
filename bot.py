import os
from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, CommandHandler, CallbackContext

TOKEN = os.getenv("7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY")
bot = Bot(token=TOKEN)

app = Flask(__name__)

@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return 'ok'

# /start command ka response
def start(update: Update, context: CallbackContext):
    update.message.reply_text("WELCOME TO VIP OWNER BOT")

# Dispatcher set karna
dispatcher = Dispatcher(bot, None, workers=0, use_context=True)
dispatcher.add_handler(CommandHandler("start", start))

@app.route('/')
def index():
    return "VIP OWNER BOT RUNNING"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    bot.set_webhook(f"Render Dashboard https://share.google/L7q2X2bEiYTsGp95J/{TOKEN}")
    app.run(host='0.0.0.0', port=port)
