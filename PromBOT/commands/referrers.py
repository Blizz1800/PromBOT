from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .consts import BTS
from . import DB, analytics
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
        name = DB['users'].find_one({'t_id': id})['name']
        btns = [
            [BTS['FOLLOWERS']],
            [name, BTS['REFERIDOS']['KEY']],
            [BTS['MONEY']['GET'], BTS['MONEY']['POST']]
        ]
        await context.bot.send_message(chat_id=id, text="Ya estamos de vuelta!!", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        return 0
    return 1