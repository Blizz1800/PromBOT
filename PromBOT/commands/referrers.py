from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .consts import BTS
from . import DB, analytics, control
from .cmd_handlers import get_referidosV2, referir

async def refferers_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = update.effective_message.text
    id = update.effective_chat.id
    if msg == BTS['REFERIDOS']['GET']:
        analytics.button_press(BTS['REFERIDOS']['GET'], update.effective_chat.id)
        await get_referidosV2(update, context)
    elif msg == BTS['REFERIDOS']['POST']:
        analytics.button_press(BTS['REFERIDOS']['POST'], update.effective_chat.id)
        await referir(update, context)
    elif msg == BTS['BACK']:
        return await control('START:2', update, context, 0)
    return 1