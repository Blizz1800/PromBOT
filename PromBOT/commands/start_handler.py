from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

from .consts import BTS, TOKEN_NAME, get_msg
from . import DB, cmd_handlers, code, start

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    name = DB['users'].find_one({'t_id': update.effective_user.id})
    if name is not None:
        if name['banned']:
            await context.bot.send_message(chat_id=update.effective_user.id, text="Tu has sido baneado, x tanto no puedes usar este servicio nunca mas\nPara mas dudas contactar los administradores", reply_markup=ReplyKeyboardRemove())
            return -1
        name = name['name']
    else:
        await start.start(update=update, context=context, start_msg=False)
        name = DB['users'].find_one({'t_id': update.effective_user.id})['name']

    if msg == name:
        return await cmd_handlers.get_info(update, context) # 0
    elif msg == BTS['REFERIDOS']['KEY']:
        return await cmd_handlers.get_referidos(update, context) # 1
    elif msg == BTS['FOLLOWERS']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    elif msg == BTS['MONEY']['GET']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    elif msg == BTS['MONEY']['POST']:
        return await cmd_handlers.money.ganar(update=update, context=context) # 2        
    else:
        p = get_msg('START', user=update.effective_user.full_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se reconoce su entrada", reply_markup=p['BTN'], parse_mode=p['MARKDOWN'])
    return 0
        
async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Usted debe ingresar al grupo `GRUPO` e invitar `X` cantidad de referidos")
    