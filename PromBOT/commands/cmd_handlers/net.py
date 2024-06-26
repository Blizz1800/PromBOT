from telegram import Update, ReplyKeyboardMarkup, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from PromBOT.commands import DB, consts, control

async def more_ways(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await control('MORE_WAYS', update=update, context=context)

async def tlgm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await control('TLGM', update=update, context=context)

async def whts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await control('WHTS', update=update, context=context)

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
    # print(msg)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=msg['MSG'],
        reply_markup=msg['BTN'],
        parse_mode=msg['MARKDOWN']
    )
