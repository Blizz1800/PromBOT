from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from .consts import BTS, TOKEN_NAME
from . import DB, start_handlers


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    if msg == BTS['INFO']:
        await start_handlers.get_info(update, context, DB)        
    elif msg == BTS['REFERIDOS']:
        await start_handlers.get_referidosV2(update, context, DB)
    elif msg == BTS['REFERIR']:
        await start_handlers.referir(update, context)
    return 0
        
async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text="Button was pressed")
    