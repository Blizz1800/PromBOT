from telegram import Update, constants, Bot, ReplyKeyboardMarkup
from telegram.ext import ContextTypes

from . import DB, control, analytics
from .consts import BTS, get_msg, MARKDOWN, ADMINS

async def base_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message.text

    if msg == BTS['RIFAS']['GET']:
        analytics.button_press(BTS['RIFAS']['GET'], update.effective_chat.id)
        await get_info(update, context)
    elif msg == BTS['RIFAS']['POST']:
        analytics.button_press(BTS['RIFAS']['POST'], update.effective_chat.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    elif msg == BTS['BACK']:
        return await control('START', update, context, -1)
    return 0
    

async def get_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    bot: Bot = context.bot
    rifas = DB['rifas'].find_one({})
    # print(rifas)
    if rifas is None:
        await bot.send_message(chat_id=update.effective_chat.id, parse_mode=MARKDOWN, text="No hay rifas en este momento...😥")
        for i in ADMINS:
            await bot.send_message(chat_id=i, parse_mode=MARKDOWN, text="No hay rifas en la base de datos!!!")
        # raise Exception("No hay rifas en la DB")
        return
    if not rifas['active']:
        await bot.send_message(chat_id=update.effective_chat.id, parse_mode=MARKDOWN, text="No hay rifas en este momento...😥")
        return 
        
    ignore = ['_id']
    txt = f"Estos son los datos de la rifa actual:\n"
    for k in rifas.keys():
        if k in ignore: 
            continue
        txt += f".    _{k}_: *{rifas[k]}*\n"
    await bot.send_message(chat_id=update.effective_chat.id, parse_mode=MARKDOWN, text=txt)
