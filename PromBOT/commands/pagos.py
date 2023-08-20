from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from . import DB
from .consts import get_msg, ADMINS, BTS

from pprint import pprint

MANY = 3

async def get_pends(update, context, index, item, l_index=0):
    global MANY
    b = False
    btns = [[InlineKeyboardButton(BTS['INLINE']['PAGO'], callback_data=f"{BTS['INLINE']['PAGO']}:{item['_id']}")]]
    i = max(index, l_index) - min(index, l_index)
    long = context.chat_data['long']
    if (i+1) % MANY == 0 and index != long:
        btns.append([InlineKeyboardButton(BTS['INLINE']['MORE'], callback_data=f"{BTS['INLINE']['MORE']}:{index}")])
        b = True
    text = f"_{(i+1)+(l_index)}_.\n"
    for i in item.keys():
        if i == "_id":
            continue
        text += "     *{}*: _{}_\n".format(i, item[i])
    await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(btns), parse_mode="Markdown", text=text)
    return b

async def get_more(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    pendientes = context.chat_data['pagos']
    i = int(data.split(':')[1])+1
    await query.edit_message_text(text=query.message.text_markdown, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[query.message.reply_markup.inline_keyboard[0][0]]]))

    for index, item in enumerate(pendientes, i):
        if await get_pends(update, context, index, item, i):
            break

async def get_pays(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pendientes = DB['pagos'].find({"pagado": False})
    context.chat_data['pagos'] = pendientes
    pends_len = DB['pagos'].count_documents({"pagado": False})
    context.chat_data['long'] = pends_len
    if pends_len == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No hay pagos pendientes")
        return
    global MANY
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Mostrando {MANY}/{pends_len} pagos pendientes")
    for index, item in enumerate(pendientes):
        if await get_pends(update, context, index, item):
            break
