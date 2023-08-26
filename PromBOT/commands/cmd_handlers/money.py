from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from PromBOT.commands.consts import BTS
from PromBOT.commands import DB

async def ganar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    btns = []
    btns.append([BTS['NET']['YT'], BTS['NET']['IG']])
    btns.append([BTS['NET']['TLGM'], BTS['NET']['WHTS']])
    btns.append([BTS['BACK']])

    await context.bot.send_message(chat_id=update.effective_chat.id, text="Elije una red para ganar dinero ;)", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True, input_field_placeholder="Red Social"))
    return 2

def update_target(t_id:int, target: str):
    r = DB['users'].update_one({"t_id": t_id}, {"$set": {"target": target}})
    return (r.modified_count, r.matched_count)

async def extraer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    id = update.effective_chat.id
    me = DB['users'].find_one({"t_id": id})
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