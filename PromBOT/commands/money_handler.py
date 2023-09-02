from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, constants
from telegram.ext import ContextTypes
from . import DB, validate, control, analytics, get_db
from .consts import BTS, get_msg, ADMINS, TOKEN_NAME, ADMINS, CANTIDAD_EXTRAER, MESSAGES, MARKDOWN
from .cmd_handlers import net, money
import time
import random

from datetime import date

from urllib.parse import quote_plus

from pprint import pprint

from bson.objectid import ObjectId

wa_code = False      # WAnna CODE
wa_photo = False     # WAnna Photo
wa_many = False      # WAnna Many Items

async def tlgm_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    m = MESSAGES['REDES']
    base = get_msg(context.user_data['NET'])
    context.user_data['METHOD'] = data
    analytics.button_press(data, update.effective_chat.id, True)
    text = base['INST']['BOT']
    db = get_db('static')
    db = db['referrals']
    refs = list(db.find({}))

    if refs is not None and len(refs)> 0:
        kb = []
        for i in range(0, len(refs), 2):
            if not refs[i]['net'] == 'Telegram':
                continue
            e1 = InlineKeyboardButton(refs[i]['name'], refs[i]['url'])
            if i + 1 < len(refs):
                e2 = InlineKeyboardButton(refs[i+1]['name'], refs[i+1]['url'])
                kb.append([e1, e2])
            else:
                kb.append([e1])
        
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=InlineKeyboardMarkup(kb), text=m['MSG'][2])
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][3])
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
    except Exception as e: 
        print(e)
        await query.answer()
    return 0


def get_spam():
    db = get_db('static')
    spam = list(db['spam'].find({}))
    # print(spam)
    return sorted(spam, key=lambda x: x['priority'], reverse=True)


async def tlgm_spam(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    base = get_msg(context.user_data['NET'])
    # print(context.user_data['NET'])
    analytics.button_press(data, update.effective_chat.id, True)
    text = base['INST']['SPAM']
    context.user_data['METHOD'] =  data
    red = context.user_data['NET'].lower()
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
        lista = get_spam()
        if len(lista)> 0:
            for i in lista:
                url = "https://api.whatsapp.com/send?text={text}".format(text=quote_plus(i[red]))
                if red == 'tlgm':
                    url = 'tg://msg_url?url={url}&text={text}'.format(url=f"https://t.me/test_promblizzbot?start={update.effective_user.id}", text=quote_plus(i[red]))
                kb = InlineKeyboardMarkup([[InlineKeyboardButton('Compartir', url=url)]])
                await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
                await context.bot.send_message(update.effective_chat.id, f"{i[red]}", reply_markup=kb, parse_mode=MARKDOWN+'V2')
        else:
            await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
            await context.bot.send_message(update.effective_chat.id, "No tenemos publicaciones en estos momentos, por favor, vuelva mas tarde", parse_mode=MARKDOWN)
    except Exception as e:
        print(e)
        await query.answer()
    return 0

async def ig_end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    m = MESSAGES['PROOFS']
    for i in context.user_data['fotos']:
        data_id = i[0]
        kb_admin = InlineKeyboardMarkup([[InlineKeyboardButton(BTS['INLINE']['ACCEPT'], callback_data=f"{BTS['INLINE']['ACCEPT']}2|{data_id}"), InlineKeyboardButton(BTS['INLINE']['DENY'], callback_data=f"{BTS['INLINE']['DENY']}2|{data_id}")]])
        for a in ADMINS:
            await context.bot.send_photo(chat_id=a, photo=i[1], reply_markup=kb_admin)
    for i in ADMINS:
        await context.bot.send_message(chat_id=i, text="Pruebas de los comentarios del usuario `{USER}`({ID})".format(USER=update.effective_user.full_name, ID=update.effective_chat.id))
    await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][0])

async def ig_comments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    db = get_db('static')
    await query.answer()
    base = get_msg(context.user_data['NET'])
    analytics.button_press(BTS['INLINE']['COMENT'], update.effective_chat.id, True)
    context.user_data['METHOD'] =  data
    text = base['INST']['COMENT']
    pub = list(db['instagram'].find({'kind': 0}))
    if len(pub) > 0:
        pub = random.choice(pub)
        kb = [[InlineKeyboardButton(pub['name'], pub['link'])]]
        txt = "Esta es la publicacion a la que debes acceder:"
    else:
        kb = [[]]
        txt = "No hay publicaciones para acceder en estos momentos."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=txt, reply_markup=InlineKeyboardMarkup(kb))
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
    except Exception as e:
        # print(e)
        await query.answer()
    return 0

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    if not isinstance(context.user_data.get('fotos', None), list):
        context.user_data['fotos'] = []
    if not context.user_data.get('count', None):
        context.user_data['count'] = 1
    context.user_data['count'] += 1

    method = context.user_data.get('METHOD', None)
    # print('User Data: ' + str(context.user_data))
    # print(context.user_data['METHOD'])
    # print(method)

    data_id = DB['requests'].insert_one(
                {
                    "t_id": update.effective_chat.id,
                    "t_im_id": photo.file_id,
                    "t_im_uid": photo.file_unique_id,
                    "status": 0,
                    "admin": None,
                    'method': method
                }
            ).inserted_id
    context.user_data['fotos'].append([data_id, photo.file_id])
    m = MESSAGES['PROOFS']
    await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][0].format(CMD='/end'))

async def envio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo
    if not photo and len(photo) <= 0:
        return await control('SEND', update, context, 1)

    db_id = context.user_data['db_id']
    DB['pagos'].update_one({"_id": ObjectId(db_id)},
        {
            "$set": {
                'pagado': True,
                'prueba': photo[-1].file_unique_id
            }
        }
    )
    me = DB['users'].find_one({'t_id': context.user_data['u_id']})
    limit_b = me['limit_b']
    delta = me['dA']

    x = limit_b + delta
    y = x % 5
    if y > 2:
        limit_b = x + (5 - y)
    else:
        limit_b = x - y
    delta += 5

    DB['users'].update_one(
        {'t_id': context.user_data['u_id']},
        {
            '$inc': {
                'token_b': -context.user_data['pago'],
                'extractions': 1,
                },
            '$set': {
                'limit_b': limit_b,
                'dA': delta
            }
        })
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Se esta enviando al usuario su aviso de pago, por favor esperar")
    m = MESSAGES['SEND']
    await context.bot.send_photo(chat_id=context.user_data['u_id'], photo=photo[-1], caption=m['MSG'][1])
    return -1
        
async def aviso_pago(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    context.user_data['db_id'] = data.split(':')[1]
    pago = DB['pagos'].find_one({"_id": ObjectId(context.user_data['db_id'])})
    context.user_data['pago'] = pago['amount']
    context.user_data['u_id'] = pago['t_id']
    if pago['pagado']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Ya ha sido pagado")
        return -1
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Por favor, envia una prueba el usuario de su pago")
    return 1

async def extract(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    id = update.effective_chat.id
    me = DB['users'].find_one({'t_id': id})
    p = get_msg('START', user=update.effective_user.full_name)
    # print(extract)
    target = me['target']
    obj = ''
    t = validate(target)
    if t >= 0:
        if t == 0:
            obj = 'tarjeta'
        else:
            obj = "celular"
    else:
        # print('\tinvalid...')
        return await control('EXTRACT:1', update, context, 2, target)
    try:
        amount = int(msg)
        if me['token_b'] >= me['limit_b']:
            if (me['token_b'] - amount) < 0:
                return await control('EXTRACT:2', update, context, -1, me['token_b'], TOKEN_NAME[1])
                
            id_db= DB['pagos'].insert_one({
                "t_id": id,
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "amount": amount,
                "prueba": None,
                "pagado": False,
                "objetivo": target
            }).inserted_id
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton(BTS['INLINE']['PAGO'], callback_data=f"{BTS['INLINE']['PAGO']}:{id_db}")]
            ])
            for i in ADMINS:
                await context.bot.send_message(chat_id=i, reply_markup=btn, parse_mode="Markdown", text=f"⚠️🫣*Houston, tenemos un problema*😬⚠️\n\nEl usuario {me['name']}({me['t_id']}), ha solicitado de {amount}{TOKEN_NAME[1]} su pago hacia su {obj} `{target}`!!😱😡")
            m = MESSAGES['EXTRACT']
            await context.bot.send_message(chat_id=id, reply_markup=p['BTN'], text=m['MSG'][2])
        else:
            # await control('EXTRACT:4', update, context, reply=p['BTN'], LIMIT_B=me["limit_b"], TK_N=TOKEN_NAME[1])
            m = MESSAGES['EXTRACT']
            await context.bot.send_message(chat_id=id, reply_markup=p['BTN'], text=m['MSG'][3].format(LIMIT_B=me['limit_b'], TK_N=TOKEN_NAME[1], MANY=me['token_b']))
    except ValueError as e:
        print(e)
        await context.bot.send_message(chat_id=id, text=f'"{msg}" NO es un numero')
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(),parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(MIN=me['limit_b'], TK=TOKEN_NAME[1]))
        return 0
    return -1

async def target_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    me = DB['users'].find_one({'t_id':  update.effective_user.id})
    m = MESSAGES['EXTRACT']
    if msg == BTS['YES']:
        # print(1)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(MIN=me['limit_b'], TK=TOKEN_NAME[1], MANY=me['token_b']))
        return 0
    elif msg == BTS['NO']:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), text=m['MSG'][4])
        return 1
    else:
        money.update_target(update.effective_chat.id, msg)
        yes_no_kb = ReplyKeyboardMarkup([[BTS['YES'], BTS['NO']]], resize_keyboard=True)
        print(8)
        await context.bot.send_message(update.effective_chat.id, reply_markup=yes_no_kb, text=m['MSG'][5].format(msg))
        return 1

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['wa_photo'] = False
    context.user_data['wa_code'] = False
    context.user_data['wa_many'] = False
    query = update.callback_query
    data = query.data
    await query.answer()
    db = get_db('static')
    base = get_msg(context.user_data['NET'])    # Selecciona Youtube o Instagram automaticamente
    # print(base)
    #   YOUTUBE
    if data == BTS['INLINE']['SUB']:
        analytics.button_press(BTS['INLINE']['UPDATE'], update.effective_chat.id, True)
        text = base['INST']['SUB']
        red = 1
        context.user_data['wa_photo'] = True
    elif data == BTS['INLINE']['CODE']:
        analytics.button_press(BTS['INLINE']['CODE'], update.effective_chat.id, True)
        text = base['INST']['CODE']
        context.user_data['wa_code'] = True
        red = 4
    #   INSTAGRAM
    elif data == BTS['INLINE']['FOLLOW']:
        analytics.button_press(BTS['INLINE']['FOLLOW'], update.effective_chat.id, True)
        text = base['INST']['FOLLOW']
        context.user_data['wa_photo'] = True
        red = 2
    elif data == BTS['INLINE']['REELS']:
        analytics.button_press(BTS['INLINE']['REELS'], update.effective_chat.id, True)
        text = base['INST']['REELS']
        context.user_data['wa_code'] = True
        red = 3
    context.user_data['METHOD'] =  data
    
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
        if red == 1:
            chanels = list(db['youtube'].find({'kind': 1}))
            kb = []
            for i in chanels:
                kb.append([InlineKeyboardButton(i['name'], i['link'])])
            if len(kb) > 0:
                await context.bot.send_message(update.effective_chat.id, "Aqui les presentamos la lista de canales📂 para suscribirse📲:", reply_markup=InlineKeyboardMarkup(kb))
            else: 
                await context.bot.send_message(update.effective_chat.id, "No tenemos canales disponibles en estos momentos", reply_markup=InlineKeyboardMarkup(kb))
        elif red == 2:
            chanels = list(db['instagram'].find({'kind': 1}))
            kb = []
            for i in chanels:
                kb.append([InlineKeyboardButton(i['name'], i['link'])])
            if len(kb) > 0:
                await context.bot.send_message(update.effective_chat.id, "Aqui les presentamos la lista de cuentas👤 para seguir:", reply_markup=InlineKeyboardMarkup(kb))
            else:
                await context.bot.send_message(update.effective_chat.id, "No tenemos cuentas👤 disponibles en estos momentos😢", reply_markup=InlineKeyboardMarkup(kb))
        elif red == 3:
            chanels = list(db['instagram'].find({'kind': 2}))
            kb = []
            for i in chanels:
                kb.append([InlineKeyboardButton(i['name'], i['link'])])
            if len(kb) > 0:
                await context.bot.send_message(update.effective_chat.id, "Aqui les presentamos la lista de publicaciones📑 para encontrar codigos:", reply_markup=InlineKeyboardMarkup(kb))
            else:
                await context.bot.send_message(update.effective_chat.id, "❌No tenemos publicaciones 📤 en estos momentos 👁‍🗨", reply_markup=InlineKeyboardMarkup(kb))
        elif red == 4:
            chanels = list(db['youtube'].find({'kind': 0}))
            kb = []
            for i in chanels:
                kb.append([InlineKeyboardButton(i['name'], i['link'])])
            if len(kb) > 0:
                await context.bot.send_message(update.effective_chat.id, "📹Aqui les presentamos la lista de videos📼 para encontrar codigos:", reply_markup=InlineKeyboardMarkup(kb))
            else:
                await context.bot.send_message(update.effective_chat.id, "❌No tenemos videos 🖥 en estos momentos 👁‍🗨", reply_markup=InlineKeyboardMarkup(kb))
    except Exception as e:
        # print(e)
        await query.answer()

async def admin_btn_v2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    await query.answer()
    # print(data)
    btn, _id = tuple(data.split('|'))

    admin = DB['requests'].find_one({"_id": ObjectId(_id)})
    photo = admin['t_im_id']
    user = admin['t_id']
    method = admin['method']
    admin = admin['admin']

    admin = DB['users'].find_one({"t_id": admin})
    if admin:
        if admin['user']:
            admin = admin['user']
        else:
            admin = admin['name']
        await query.edit_message_caption(f"Esta prueba prueba ya fue requisada por {admin}")
        return 
    is_accept = False
    if btn == f"{BTS['INLINE']['ACCEPT']}2":
        is_accept = True
        status = 1
        inc = 1
        warn = 0
        # ban = False
    elif btn == f"{BTS['INLINE']['DENY']}2":
        u = DB['users'].find_one({"t_id": user})
        if u['warns'] >= 3:
            warn = 0
            inc = -2
        else:
            warn = 1
            inc = 0

        status = -1
        # ban = True

    DB['requests'].update_one(
        {
            "_id": ObjectId(_id),
        },{
            "$set": {
                "status": status,
                "admin": update.effective_chat.id
            }
        }
    )

    DB['users'].update_one({"t_id": user}, {"$inc": {"token_a": inc, "warns": warn}})

    if inc > 0 :
        m = method
        if m == BTS['INLINE']['FOLLOW']:
            m = analytics.TK_RED.INSTAGRAM_FOLL
        elif m == BTS['INLINE']['REELS']:
            m = analytics.TK_RED.INSTAGRAM_REEL
        elif m == BTS['INLINE']['COMENT']:
            m = analytics.TK_RED.INSTAGRAM_COM
        elif m == BTS['INLINE']['CODE']:
            m = analytics.TK_RED.YOUTUBE_CODES
        elif m == BTS['INLINE']['SUB']:
            m = analytics.TK_RED.YOUTUBE_SUB
        analytics.earn_tk(m, user, inc, analytics.TK.A)

    if status > 0:
        stat = "aceptado"
        emoji = '✨'
        rec = f". Ha recibido *+{inc} {TOKEN_NAME[1]}*"
    else:
        stat = "denegado"
        emoji = '😢'
        rec = "."
    try:
        await query.edit_message_caption(f"Usted ha {stat} esta solicitud")
    except Exception as e:
        print(e)
        await query.answer()
    await context.bot.send_chat_action(user, constants.ChatAction.UPLOAD_PHOTO)
    await context.bot.send_photo(chat_id=user, photo=photo, caption=f"Se ha {stat} su foto{emoji}{rec}", parse_mode=MARKDOWN)
    if not is_accept:
        m = MESSAGES['WARNS']
        if inc >= 0:
            await context.bot.send_chat_action(user, constants.ChatAction.TYPING)
            await context.bot.send_message(chat_id=user, text=m['MSG'][0].format(u['warns']))
        else:
            await context.bot.send_chat_action(user, constants.ChatAction.TYPING)
            await context.bot.send_message(chat_id=user, text=m['MSG'][1].format(u['warns'], inc * -1, TOKEN_NAME[1]))
    # return -1


async def admin_btn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    await query.answer()
    btn, _id = tuple(data.split('|'))

    admin = DB['requests'].find_one({"_id": ObjectId(_id)})
    user = admin['t_id']
    method = admin['method']
    admin = admin['admin']

    admin = DB['users'].find_one({"t_id": admin})
    if admin:
        if admin['user']:
            admin = admin['user']
        else:
            admin = admin['name']
        await query.edit_message_caption(f"Este mensaje ya fue aprobado por {admin}")
        return 
    # status = 100
    if btn == BTS['INLINE']['ACCEPT']:
        status = 1
        inc = 1
        ban = False
    elif btn == BTS['INLINE']['DENY']:
        status = -1
        ban = True
        inc = 0
    
    DB['requests'].update_one(
        {"_id": ObjectId(_id)},{
            "$set": {
                "status": status,
                "admin": update.effective_chat.id
            }
        }
    )
    # analytics.earn_tk(analytics.TK_RED.)
    DB['users'].update_one({"t_id": user}, {"$inc": {"token_a": inc}, "$set":{"banned": ban}})
    if inc > 0 :
        m = method
        if m == BTS['INLINE']['FOLLOW']:
            m = analytics.TK_RED.INSTAGRAM_FOLL
        elif m == BTS['INLINE']['REELS']:
            m = analytics.TK_RED.INSTAGRAM_REEL
        elif m == BTS['INLINE']['COMENT']:
            m = analytics.TK_RED.INSTAGRAM_COM
        elif m == BTS['INLINE']['CODE']:
            m = analytics.TK_RED.YOUTUBE_CODES
        elif m == BTS['INLINE']['SUB']:
            m = analytics.TK_RED.YOUTUBE_SUB
        analytics.earn_tk(m, user, inc, analytics.TK.A)

    if status > 0:
        stat = "aceptado ⭐"
        rec = f". Ha recibido *+{inc} {TOKEN_NAME[0]}* 💰"
    else:
        stat = "denegado 😢"
        rec = "."
    try:
        await query.edit_message_caption(f"Usted ha {stat} esta solicitud")
    except Exception as e:
        # print(e)
        await query.answer()
    await context.bot.send_chat_action(user, constants.ChatAction.TYPING)
    await context.bot.send_message(chat_id=user, text=f"Se ha {stat} su solicitud{rec}", parse_mode=MARKDOWN)

async def extract_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message.text

    me = DB['users'].find_one({'t_id': update.effective_user.id})
    yes_no_kb = ReplyKeyboardMarkup([[BTS['YES'], BTS['NO']]], resize_keyboard=True)

    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    if msg == BTS['YES']:
        # print(2)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(MIN=me['limit_b'], TK=TOKEN_NAME[1], MANY=me['token_b']))
        return 0
    elif msg == BTS['NO']:
        kb = ReplyKeyboardMarkup([
            [ BTS['CANCEL'] ]
            ], resize_keyboard=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=kb, parse_mode="Markdown", text=f"📥Introduzca el destino 💳 donde desea recibir su dinero. 💰")
    elif msg == BTS['CANCEL']:
        return await control('START:2', update, context, -1)
    else:
        money.update_target(update.effective_chat.id, msg)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=yes_no_kb, text=f'🪪Es esta su nueva direccion de destino para recibir sus pagos?💰\n\n`{msg}`', parse_mode=MARKDOWN)
    return 1

async def money_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT'], BTS['NET']['IG']])
    btns.append([BTS['NET']['TLGM'], BTS['NET']['WHTS']])
    btns.append([BTS['BACK']])

    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    id = update.effective_chat.id
    msg = update.message.text
    DB['users'].update_many(
    {},
    {"$pull":{
        "codes": None
    }})
    
    context.user_data['reset'] = False
    if msg == BTS['NET']['IG']:
        context.user_data['NET'] = 'IG'
        context.user_data['reset'] = True
        await net.ig(update, context)
    elif msg == BTS['NET']['YT']:
        context.user_data['NET'] = 'YT'
        context.user_data['reset'] = True
        await net.yt(update, context)
    elif msg == BTS['NET']['TLGM']:
        context.user_data['NET'] = 'TLGM'
        context.user_data['reset'] = True
        await net.tlgm(update, context)
    elif msg == BTS['NET']['WHTS']:
        context.user_data['NET'] = 'WHTS'
        context.user_data['reset'] = True
        await net.whts(update, context)
    elif msg == BTS['MORE_WAYS']:
        context.user_data['NET'] = 'WHTS'
        context.user_data['reset'] = True
        await net.more_ways(update, context)
    elif msg == BTS['BACK']:
        context.user_data['reset'] = True
        return await control('START:2', update, context)

    if context.user_data.get('reset', False):
        context.user_data['wa_code'], context.user_data['wa_photo'], context.user_data['wa_code']  = (False, False, False)
        context.user_data['reset'] = False

    if context.user_data.get('wa_code', False):
        invalid = get_msg('INVALID_CODE')
        if msg == BTS['NO_CODE']:
            msg = get_msg('NO_CODE')['MSG']
            btns = []
            btns.append([BTS['NET']['YT'], BTS['NET']['IG']])
            btns.append([BTS['NET']['TLGM'], BTS['NET']['WHTS']])
            btns.append([BTS['BACK']])
            context.user_data['wa_code'] = False

            await context.bot.send_message(chat_id=id, text=msg, reply_markup=ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True))
            return 2
        if DB['codes'].find_one({'code': msg}):
            if DB['users'].find_one({"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]}):

                DB['users'].update_one(
                    {"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]},
                    {"$unset": {"codes.$[i]": ""}, "$inc": {"token_b": 1}},
                    array_filters=[{"i": {"$eq": msg}}])
    
                msg = get_msg('NO_CODE')['MSG']
                analytics.earn_tk(analytics.TK_RED.YOUTUBE_CODES, id, 1, analytics.TK.B)
                await context.bot.send_message(chat_id=id, text=f"📩 Usted ha enviado su código correctamente\n*+1 {TOKEN_NAME[1]}*", parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
                context.user_data['wa_code'] = False
            else:
                await context.bot.send_message(chat_id=id, text="❌ Ese código ya ha sido usado...!!")
                await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
        else:
            await context.bot.send_message(chat_id=id, text="Ese codigo no existe!")
            await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
    elif context.user_data.get('wa_photo', False):
        if update.message.photo:
            data_id = DB['requests'].insert_one(
                {
                    "t_id": id,
                    "t_im_id": update.message.photo[-1].file_id,
                    "t_im_uid": update.message.photo[-1].file_unique_id,
                    "status": 0,
                    "admin": None
                }
            ).inserted_id
            for i in ADMINS:
                await context.bot.send_photo(chat_id=i, parse_mode="Markdown", photo=update.message.photo[-1].file_id, caption=f"El usuario {update.effective_user.full_name}{id}), ha enviado esta prueba de su subscripcion", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BTS['INLINE']['ACCEPT'], callback_data=f"{BTS['INLINE']['ACCEPT']}|{data_id}"), InlineKeyboardButton(BTS['INLINE']['DENY'], callback_data=f"{BTS['INLINE']['DENY']}|{data_id}")]]))
            await context.bot.send_message(chat_id=id, parse_mode="Markdown", text="⌛️ Por favor, espere que le avisemos si su imagen cumple los requisitos", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
            return 2
        else:
            # pprint(btns)
            await context.bot.send_message(chat_id=id, text="🚫No se detecto ninguna foto😢", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        
        context.user_data['wa_photo'] = False

    return 2