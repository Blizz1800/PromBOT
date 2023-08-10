from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from PromBOT.commands.consts import BTS

async def ganar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT']])
    btns.append([BTS['NET']['IG']])
    btns.append([BTS['BACK']])

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Elije una red para ganar dinero ;)", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True, input_field_placeholder="Red Social"))
    return 2