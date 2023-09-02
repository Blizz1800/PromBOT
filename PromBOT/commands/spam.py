from telegram import Update, ReplyKeyboardMarkup, constants, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from . import get_db, control
from .consts import ADMINS, STD_MK, MESSAGES, BTS
import re
from bson import ObjectId

def format_whts(text: str):
    # Eliminar "__" si hay un inicio "__" y un final "__"
    text = re.sub(r'__(.*?)__', r'\1', text)
    # Reemplazar "`" por "```" si hay 1 o 2 "`" en grupo
    text = re.sub(r'(`+)(.*?)\1', r'```\2```', text)
    return text

def format_tlgm(text: str):
    t = re.sub(r'__(.*?)__', r'\1', text)
    t = re.sub(r'\*(.*?)\*', r'**\1**', t)
    t = re.sub(r'_(.*?)_', r'__\1__', t)
    t = re.sub(r'~(.*?)~', r'~~\1~~', t)
    return t

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id in ADMINS:
        return -1
    txt = "Por favor, inserte el mensaje para dar a compartir a los usuarios"
    await context.bot.send_message(update.effective_user.id ,txt)
    return 0

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    msg = update.message.text_markdown_v2
    whts = format_whts(msg)
    tlgm = format_tlgm(msg)
    db = get_db('static')['spam']
    db.insert_one({
        "priority": 1,
        "msg": msg,
        'tlgm': tlgm,
        'whts': whts,
        't_id': update.effective_user.id
    })
    
    await context.bot.send_message(update.effective_chat.id, "Se ha agregado su mensaje:\n\n`{}`\n\ndesea avisar a los usuarios??".format(msg), parse_mode=STD_MK+'V2', reply_markup=ReplyKeyboardMarkup([["Si", "No"]], resize_keyboard=True))
    return 1

async def advice_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()

    if msg == 'si':
        db = get_db()['users']
        users = db.find({})
        all = True
        for user in users:
            id = user['t_id']
            try:
                await context.bot.send_chat_action(id, constants.ChatAction.TYPING)
                await context.bot.send_message(id, "😃 Hey, hay nuevos mensajes 📩 para compartir 📨, pasate a verlos 😉")
            except Exception as e:
                all = False
                await context.bot.send_message(update.effective_chat.id, f"No se pudo enviar el aviso al usuario {{ {user['name']}, {id} }}, motivo: \n\n{e}")
        if all:
            await context.bot.send_message(update.effective_chat.id, "Todos los mensajes se enviaron satisfactoriamente")
        else:
            await context.bot.send_message(update.effective_chat.id, "Los mensajes se enviaron con errores")
    
    return await control('START:2', update, context, -1)

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    db = get_db('static')['spam']
    udb = get_db()['users']
    for i in db.find({}):
        await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
        user = udb.find_one({'t_id': i['t_id']})
        if not user:
            user = "Unknown"
        txt = "Agregado por: _{}_\n\nPrioridad: *{}*\n\nMensaje: `{}`".format(user['name'], i['priority'], i['msg'])
        print(txt)
        kb = InlineKeyboardMarkup(
            [[InlineKeyboardButton(BTS['INLINE']['REMOVE'], callback_data=f"rem|{i['_id']}")]]
        )
        await context.bot.send_message(update.effective_chat.id, txt, parse_mode=STD_MK+'V2', reply_markup=kb)

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    _id = data.split('|')[1]

    db = get_db('static')['spam']
    tmp = db.find_one_and_delete({'_id': ObjectId(_id)})
    print()
    print(_id)
    print(tmp)
    await query.delete_message()