from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace with your token
TOKEN = '7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY'

# Item prices
ITEMS = {
    'item1': {'name': 'Item 1', 'price': '₹50'},
    'item2': {'name': 'Item 2', 'price': '₹100'}
}

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Buy Item 1", callback_data='item1')],
        [InlineKeyboardButton("Buy Item 2", callback_data='item2')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose an item to buy:', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()

    item_key = query.data
    item = ITEMS.get(item_key)

    if item:
        message = f"You selected *{item['name']}*.\nPrice: *{item['price']}*\n\nPlease make the payment and send the screenshot to admin."
        # You can replace this with actual payment logic or auto-generation if integrated
        query.edit_message_text(text=message, parse_mode='Markdown')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()