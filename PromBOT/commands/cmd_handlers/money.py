from telegram import Update, ReplyKeyboardMarkup, constants
from telegram.ext import ContextTypes
from PromBOT.commands.consts import BTS, TOKEN_NAME
from PromBOT.commands import DB

async def ganar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT'], BTS['NET']['IG']])
    btns.append([BTS['NET']['TLGM'], BTS['NET']['WHTS']])
    btns.append([BTS['MORE_WAYS']])
    btns.append([BTS['BACK']])
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)

    await context.bot.send_message(chat_id=update.effective_chat.id, text="""Poseemos dos tipos de moneda: {A} y {B}. La moneda {B} consta de 17 {A} y esta {B} es intercambiable por 1 peso cubano 🪙, directo a la tarjeta bancaria 💳 o recarga al móvil 📲.En un futuro podremos cambiarlo en otros tipos de moneda 🪙 como MLC💶, USD💷 para que se puedan realizar compras en el exterior 💳.\n\nPor favor, elija la plataforma que mas familiarizado este con ellay siga las instrucciones para comenzar a ganar👇🏻\n(Recomendamos usar WiFi)""".format(A=TOKEN_NAME[0], B=TOKEN_NAME[1]), reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True, input_field_placeholder="Red Social"))
    return 2

def update_target(t_id:int, target: str):
    r = DB['users'].update_one({"t_id": t_id}, {"$set": {"target": target}})
    return (r.modified_count, r.matched_count)

async def extraer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    me = DB['users'].find_one({"t_id": id})
    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    if me['target']:
        kb = ReplyKeyboardMarkup([
            [BTS['YES'], BTS['NO']],
            [ BTS['CANCEL'] ]
            ], resize_keyboard=True)
        await context.bot.send_message(chat_id=id, text=f"Es este, {me['target']}, su destinatario para la extraccion? Si no es este, por favor introduzca su nuevo destinatario", reply_markup=kb                                              )
    else:
        kb = ReplyKeyboardMarkup([
            [ BTS['CANCEL'] ]
            ], resize_keyboard=True)
        await context.bot.send_message(chat_id=id, text=f"Por Favor Introduzca su destinatario para donde desea recibir el pago.", reply_markup=kb)
    return 4