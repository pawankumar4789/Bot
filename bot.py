from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# 🔐 Apna Telegram Bot Token yahan daalo
TOKEN = '7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY'

# 🎯 /start command ka function
def start(update: Update, context: CallbackContext):
    update.message.reply_text("WELCOME TO VIP OWNER BOT")

# 🚀 Bot start karne ka main function
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # /start command handler
    dp.add_handler(CommandHandler("start", start))

    # Bot start karo
    updater.start_polling()
    updater.idle()

# 🔃 Program start point
if __name__ == '__main__':
    main()
