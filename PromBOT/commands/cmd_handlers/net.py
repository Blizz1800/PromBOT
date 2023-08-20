from telegram import Update, ReplyKeyboardMarkup, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from PromBOT.commands import DB, consts

async def yt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    
    msg = consts.get_msg('YT')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg['MSG'],
        reply_markup=msg['BTN'],
        parse_mode=msg['MARKDOWN']
    )

async def ig(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    
    msg = consts.get_msg('IG')
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg['MSG'],
        reply_markup=msg['BTN'],
        parse_mode=msg['MARKDOWN']
    )
