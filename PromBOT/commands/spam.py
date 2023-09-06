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

def format_ref(text: str):
    regex = r"https://wa\.me/(\+\d+)"
    match = re.search(regex, text)
    t = None
    if match:
        t = match.group(1)
    return t

async def insert(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user.id in ADMINS:
        return -1
    txt = "Por favor, inserte el mensaje para dar a compartir a los usuarios"
    await context.bot.send_message(update.effective_user.id ,txt)
    return 0


async def insert_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['spam'] = update.message.text_markdown_v2
    txt = "Por favor, inserte el link de referencia de su usuario para la red de whatsapp"
    await context.bot.send_message(update.effective_user.id ,txt)
    return 1
    

async def advice(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    ref = update.message.text
    msg:str = context.user_data['spam']
    whts = format_whts(msg.replace('\\', ''))
    tlgm = format_tlgm(msg.replace('\\', ''))
    char_list = list('*_')
    for i in char_list:
        msg = msg.replace(f'\\{i}', i)
    db = get_db('static')['spam']
    db.insert_one({
        "priority": 1,
        "msg": msg,
        'tlgm': tlgm,
        'whts': whts,
        'ref': ref,
        'phone': format_ref(ref),
        't_id': update.effective_user.id
    })
    
    await context.bot.send_message(update.effective_chat.id, "Se ha agregado su mensaje:\n\n`{}`\n\ndesea avisar a los usuarios??".format(msg), parse_mode=STD_MK+'V2', reply_markup=ReplyKeyboardMarkup([["Si", "No"]], resize_keyboard=True))
    return 2

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
        # print(txt)
        kb = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton('⬇️', callback_data=f'prior|{i["_id"]}|-1'), InlineKeyboardButton('⬆️', callback_data=f'prior|{i["_id"]}|1')],
                [InlineKeyboardButton(BTS['INLINE']['REMOVE'], callback_data=f"rem|{i['_id']}")]
            ]
        )
        await context.bot.send_message(update.effective_chat.id, txt, parse_mode=STD_MK+'V2', reply_markup=kb)

async def prior(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    data = data.split('|')
    _id = data[1]
    oper = int(data[2])
    
    p_max, p_min = (10, 1)

    udb = get_db()['users']
    db = get_db('static')['spam']
    doc = db.find_one({'_id': ObjectId(_id)})
    priority = doc['priority']
    if (priority == p_min and oper < 0) or (priority == p_max and oper > 0):
        oper = 0

    db.find_one_and_update(
        {'_id': ObjectId(_id)},
        {
            '$inc': {
                'priority': oper
            }
        }
    )

    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    doc = db.find_one({'_id': ObjectId(_id)})
    user = udb.find_one({'t_id': doc['t_id']})
    if not user:
        user = "Unknown"
    txt = "Agregado por: _{}_\n\nPrioridad: *{}*\n\nMensaje: `{}`".format(user['name'], doc['priority'], doc['msg'])
    kb = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton('⬇️', callback_data=f'prior|{doc["_id"]}|-1'), InlineKeyboardButton('⬆️', callback_data=f'prior|{doc["_id"]}|1')],
            [InlineKeyboardButton(BTS['INLINE']['REMOVE'], callback_data=f"rem|{doc['_id']}")]
        ]
    )
    try:
        await query.edit_message_text(txt, parse_mode=STD_MK+'V2', reply_markup=kb)
    except:
        pass
    await query.answer()

async def remove(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    _id = data.split('|')[1]

    db = get_db('static')['spam']
    db.find_one_and_delete({'_id': ObjectId(_id)})
    # print()
    # print(_id)
    # print(tmp)
    await query.delete_message()