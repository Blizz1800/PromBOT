from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from . import DB
from .consts import BTS, get_msg, ADMINS, TOKEN_NAME
from .cmd_handlers import net

wa_code = False     # WAnna CODE
wa_photo = False     # WAnna Photo

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global wa_code, wa_photo
    query = update.callback_query
    data = query.data
    await query.answer()
    base = get_msg('YT')
    if data == BTS['INLINE']['SUB']:
        text = base['INST']['SUB']
        wa_photo = True
        wa_code = False
        print(f"{BTS['INLINE']['SUB']} selected")
    elif data == BTS['INLINE']['CODE']:
        text = base['INST']['CODE']
        wa_photo = False
        wa_code = True
        print(f"{BTS['INLINE']['CODE']} selected")
    try:
        await query.edit_message_text(text=text, parse_mode=base['MARKDOWN'], reply_markup=base['BTN'])
    except:
        pass

async def admin_btn(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    data = query.data
    await query.answer()
    btn, user = tuple(query.data.split(':'))
    if btn == BTS['INLINE']['ACCEPT']:
        pass
    elif btn == BTS['INLINE']['DENY']:
        pass
    
async def money_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT']])
    btns.append([BTS['NET']['IG']])
    btns.append([BTS['BACK']])
    global wa_code, wa_photo
    id = update.effective_chat.id
    msg = update.message.text
    if not wa_code and not wa_photo:
        if msg == BTS['NET']['IG']:
            await context.bot.send_message(chat_id=id, text="Under Construction")
        elif msg == BTS['NET']['YT']:
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
            await context.bot.send_message(chat_id=id, text=msg, reply_markup=ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True))
            return 2
        if DB['codes'].find_one({'code': msg}):
            if DB['users'].find_one({"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]}):
                a = DB['users'].update_one(
                    {"$and":[{"t_id": id}, {"codes": {"$elemMatch": {"$eq": msg}}}]},
                    {"$unset": {"codes.$[i]": ""}, "$inc": {"token_a": 1}},
                    array_filters=[{"i": {"$eq": msg}}])
    
                msg = get_msg('NO_CODE')['MSG']
                
                await context.bot.send_message(chat_id=id, text=f"Usted ha enviado su código correctamente\n*\+1 {TOKEN_NAME[0]}*", parse_mode="MarkdownV2", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
                wa_code = False
            else:
                await context.bot.send_message(chat_id=id, text="Ese codigo ya ha sido usado >:(")
                await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
        else:
            await context.bot.send_message(chat_id=id, text="Ese codigo no existe!")
            await context.bot.send_message(chat_id=id, text=invalid['MSG'], reply_markup=invalid['BTN'], parse_mode=invalid['MARKDOWN'])
    elif wa_photo:
        if update.message.photo:
            for i in ADMINS:
                await context.bot.send_photo(chat_id=i, parse_mode="MarkdownV2", photo=update.message.photo[-1], caption=f"El usuario {update.effective_chat.full_name}\({id}\), ha enviado esta prueba de su subscripcion", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(BTS['INLINE']['ACCEPT'], callback_data=f"{BTS['INLINE']['ACCEPT']}:{id}"), InlineKeyboardButton(BTS['INLINE']['DENY'], callback_data=f"{BTS['INLINE']['DENY']}:{id}")]]))
            await context.bot.send_message(chat_id=id, parse_mode="MarkdownV2", text="Por favor, espere que le avisemos si su imagen cumple los requisitos", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        else:
            await context.bot.send_message(chat_id=id, text="No photo in message", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
        
        wa_photo = False

    return 2