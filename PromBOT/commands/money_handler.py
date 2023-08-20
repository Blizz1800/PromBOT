from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes
from . import DB, validate, control
from .consts import BTS, get_msg, ADMINS, TOKEN_NAME, ADMINS, CANTIDAD_EXTRAER
from .cmd_handlers import net, money
import time

from pprint import pprint

from bson.objectid import ObjectId

wa_code = False      # WAnna CODE
wa_photo = False     # WAnna Photo

async def envio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo
    if not photo and len(photo) <= 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se ha detectado una foto, por favor, reenviela")
        return 1

    db_id = context.user_data['db_id']
    DB['pagos'].update_one({"_id": ObjectId(db_id)},
        {
            "$set": {
                'pagado': True,
                'prueba': photo[-1].file_unique_id
            }
        }
    )
    DB['users'].update_one({'t_id': context.user_data['u_id']}, {'$inc': {'token_b': -context.user_data['pago']}})
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Se esta enviando al usuario su aviso de pago, por favor esperar")
    await context.bot.send_photo(chat_id=context.user_data['u_id'], photo=photo[-1], caption="Su pago ha sido enviado a su destino, por favor espere paciente a recibirlo")
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

    target = me['target']
    obj = ''
    t = validate(target)
    if t >= 0:
        if t == 0:
            obj = 'tarjeta'
        else:
            obj = "celular"
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="`{}` no es una direccion valida, por favor, introduzca una direccion a la q podamos enviar su dinero (Numero de telefono o Tarjeta de Banco)".format(target), reply_markup=ReplyKeyboardMarkup([[BTS['CANCEL']]], True), parse_mode='Markdown')
        return 2
    try:
        amount = int(msg)
        if (me['token_b'] - amount) >= 10:
            # DB['users'].update_one({'t_id': id}, {'$inc': {'token_b': -amount}})
            
           
            id_db= DB['pagos'].insert_one({
                "t_id": id,
                "time": time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()),
                "amount": amount,
                "prueba": None,
                "pagado": False
            }).inserted_id
            btn = InlineKeyboardMarkup([
                [InlineKeyboardButton(BTS['INLINE']['PAGO'], callback_data=f"{BTS['INLINE']['PAGO']}:{id_db}")]
            ])
            for i in ADMINS:
                await context.bot.send_message(chat_id=i, reply_markup=btn, parse_mode="Markdown", text=f"⚠️🫣*Houston, tenemos un problema*😬⚠️\n\nEl usuario {me['name']}({me['t_id']}), ha solicitado de {amount}{TOKEN_NAME[1]} su pago hacia su {obj} `{target}`!!😱😡")
            await context.bot.send_message(chat_id=id, reply_markup=p['BTN'], text=f'🥺Su solicitud esta siendo procesada por los 🤵🏻‍♂️admin, por favor espere...👨🏻‍💻')
        else:
            await context.bot.send_message(chat_id=id, reply_markup=p['BTN'], text=f'Debe tener al menos 10 {TOKEN_NAME[1]} para efectuar el pago, y su valor neto debe ser mayor a 10 {TOKEN_NAME[1]}.\n\nEsto significa que usted debera dejar en su cuenta al menos 10 {TOKEN_NAME[1]} para efectuar el pago. Si su cantidad de {TOKEN_NAME[1]} es menor que 10, o su solicitud de pago llega a ser menor que 10 {TOKEN_NAME[1]}, no se llevara a cabo')
    except ValueError as e:
        await context.bot.send_message(chat_id=id, text=f'"{msg}" NO es un numero \n\n{e}')
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(),parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(TK=TOKEN_NAME[1]))
        return 0
    return -1

async def target_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    if msg == BTS['YES']:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(TK=TOKEN_NAME[1]))
        return 0
    elif msg == BTS['NO']:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), text="Por favor re_introduzca su direccion de destinatario")
        return 1
    else:
        money.update_target(update.effective_chat.id, msg)
        yes_no_kb = ReplyKeyboardMarkup([[BTS['YES'], BTS['NO']]], resize_keyboard=True)

        await context.bot.send_message(update.effective_chat.id, reply_markup=yes_no_kb, text="Usted ha introducido {} como nuevo destino, este correcto?".format(msg))
        return 1

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global wa_code, wa_photo
    wa_photo = False
    wa_code = False
    query = update.callback_query
    data = query.data
    await query.answer()
    base = get_msg(context.user_data['NET'])    # Selecciona Youtube o Instagram automaticamente
    #   YOUTUBE
    if data == BTS['INLINE']['SUB']:
        text = base['INST']['SUB']
        wa_photo = True
    elif data == BTS['INLINE']['CODE']:
        text = base['INST']['CODE']
        wa_code = True
    #   INSTAGRAM
    elif data == BTS['INLINE']['COMENT']:
        text = base['INST']['COMENT']
    elif data == BTS['INLINE']['FOLLOW']:
        text = base['INST']['FOLLOW']
    elif data == BTS['INLINE']['REELS']:
        text = base['INST']['REELS']
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
    except:
        pass

async def admin_btn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    await query.answer()
    btn, _id = tuple(query.data.split('|'))

    admin = DB['requests'].find_one({"_id": ObjectId(_id)})
    user = admin['t_id']
    admin = admin['admin']

    admin = DB['users'].find_one({"t_id": admin})
    if admin:
        if admin['user']:
            admin = admin['user']
        else:
            admin = admin['name']
        await query.edit_message_caption(f"Este mensaje ya fue aprobado por {admin}")
        return 

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
    DB['users'].update_one({"t_id": user}, {"$inc": {"token_b": inc}, "$set":{"banned": ban}})
    if status > 0:
        stat = "aceptado"
        rec = f". Ha recibido *+{inc} {TOKEN_NAME[1]}*"
    else:
        stat = "denegado"
        rec = "."
    await query.edit_message_caption(f"Usted ha {stat} esta solicitud")
    await context.bot.send_message(chat_id=user, text=f"Se ha {stat} su solicitud{rec}")

async def extract_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    msg = update.message.text

    yes_no_kb = ReplyKeyboardMarkup([[BTS['YES'], BTS['NO']]], resize_keyboard=True)

    if msg == BTS['YES']:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown", text=CANTIDAD_EXTRAER.format(TK=TOKEN_NAME[1]))
        return 0
    elif msg == BTS['NO']:
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=ReplyKeyboardRemove(), parse_mode="Markdown", text=f"Introduzca el destino donde desea recibir su dinero.")
    elif msg == BTS['CANCEL']:
        return await control('START:2', update, context, -1)
    else:
        money.update_target(update.effective_user.id, msg)
        await context.bot.send_message(chat_id=update.effective_chat.id, reply_markup=yes_no_kb, text=f'Es esta su nueva direccion de destino para recibir sus pagos?\n\n{msg}')
    return 1

async def money_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT']])
    btns.append([BTS['NET']['IG']])
    btns.append([BTS['BACK']])
    global wa_code, wa_photo
    id = update.effective_chat.id
    msg = update.message.text
    DB['users'].update_many(
        {},
        {"$pull":{
            "codes": None
        }}
    )
    if not wa_code and not wa_photo:
        if msg == BTS['NET']['IG']:
            context.user_data['NET'] = 'IG'
            await net.ig(update, context)
        elif msg == BTS['NET']['YT']:
            context.user_data['NET'] = 'YT'
            await net.yt(update, context)
        elif msg == BTS['BACK']:
            p = get_msg('START', user=update.effective_user.full_name)
            await context.bot.send_message(chat_id=id, text=p['MSG'], reply_markup=p['BTN'], parse_mode=p['MARKDOWN'])
            return 0
    elif wa_code:
        invalid = get_msg('INVALID_CODE')
        if msg == BTS['NO_CODE']:
            msg = get_msg('NO_CODE')['MSG']
            btns = []
            btns.append([BTS['NET']['YT']])
            btns.append([BTS['NET']['IG']])
            btns.append([BTS['BACK']])
            wa_code = False

            await context.bot.send_message(chat_id=id, text=msg, reply_markup=ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True))
            return 2
        if DB['codes'].find_one({'code': msg}):
            if DB['users'].find_one({"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]}):
                a = DB['users'].update_one(
                    {"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]},
                    {"$unset": {"codes.$[i]": ""}, "$inc": {"token_a": 1}},
                    array_filters=[{"i": {"$eq": msg}}])
    
                msg = get_msg('NO_CODE')['MSG']
                
                await context.bot.send_message(chat_id=id, text=f"Usted ha enviado su código correctamente\n*+1 {TOKEN_NAME[0]}*", parse_mode="Markdown", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
                wa_code = False
            else:
                await context.bot.send_message(chat_id=id, text="Ese codigo ya ha sido usado >:(")
                await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
        else:
            await context.bot.send_message(chat_id=id, text="Ese codigo no existe!")
            await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
    elif wa_photo:
        if update.message.photo:
            data_id = DB['requests'].insert_one(
                {
                    "t_id": id,
                    "t_im_id": update.message.photo[-1].file_id,
                    "status": 0,
                    "admin": None
                }
            ).inserted_id
            for i in ADMINS:
                await context.bot.send_photo(chat_id=i, parse_mode="Markdown", photo=update.message.photo[-1].file_id, caption=f"El usuario {update.effective_chat.full_name}{id}), ha enviado esta prueba de su subscripcion", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BTS['INLINE']['ACCEPT'], callback_data=f"{BTS['INLINE']['ACCEPT']}|{data_id}"), InlineKeyboardButton(BTS['INLINE']['DENY'], callback_data=f"{BTS['INLINE']['DENY']}|{data_id}")]]))
            await context.bot.send_message(chat_id=id, parse_mode="Markdown", text="Por favor, espere que le avisemos si su imagen cumple los requisitos", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        else:
            await context.bot.send_message(chat_id=id, text="No photo in message", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        
        wa_photo = False

    return 2