from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from .consts import BTS, get_msg

async def money_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message.text
    if msg == BTS['NET']['IG']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction")
    elif msg == BTS['NET']['YT']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction")
    elif msg == BTS['BACK']:
        p = get_msg('START', user=update.effective_user.full_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=p['MSG'], reply_markup=ReplyKeyboardMarkup(p['BTN'], resize_keyboard=True), parse_mode=p['MARKDOWN'])
        return 0
    return 2