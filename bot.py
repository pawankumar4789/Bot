from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import requests

# Replace with your token
TOKEN = '7744875151:AAF8P1vSd8awHrmaGmWQiI6d-S_fgoPvLkY'

# Replace with your payment gateway and key generation logic
PAYMENT_API_URL = 'YOUR_PAYMENT_GATEWAY_URL'
KEY_GENERATION_API_URL = 'https://bgmiloader.2ezy.win/keys/generate'

def start(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton("Buy Item", callback_data='buy_item')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.
