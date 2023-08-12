from telegram import Update
from telegram.ext import ContextTypes

from . import DB
from .consts import get_msg, ADMINS

import hashlib
import time

async def gen_msg(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await context.bot.send_message(chat_id=update.message.chat_id, text="Digite la cantidad de codigos a generar:")
    return 0

async def gen_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if update.effective_chat.id in ADMINS:
        if update.message.text == '/cancel':
            p = get_msg('START', user=update.effective_user.full_name)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=p['MSG'], reply_markup=p['BTN'], parse_mode=p['MARKDOWN'])
            return -1
        DB['users'].update_many({'codes': {'$exists': False}}, {'$set': {'codes': []}})
        # if DB['codes'].find_one({'code': {'$exists': True}}) is None:
        #     DB['codes'].insert_one({
        #         'code': 
        #         })
        try:
            LEN = update.message.text
            c_len = 3
            msg = "Los codigos generados son: \n"
            for i in range(0, int(LEN)):
                t = int(round(time.time() * 1000))
                while(t == int(round(time.time() * 1000))):
                    continue
                code = hashlib.md5(str(t).encode('utf-8')).hexdigest()
                code = f"{code[:c_len]}{code[c_len*-1:]}"
                DB['codes'].insert_one({'code': code})
                DB['users'].update_many({}, {'$push': {'codes': code}})
                msg += f"\.    `{code}`\n" 
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg, parse_mode='MarkdownV2')
        except Exception as e:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Error: `{e}`, re\-enter number\.\.\. or type /cancel', parse_mode='MarkdownV2')
        return -1
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Usted no es un administrador, por favor no lo intente de nuevo")
        for i in ADMINS:
            context.bot.send_message(chat_id=i, text="El usuario con id: `{}` ha intentado una violacion de acceso".format(update.effective_chat.id))
        return -1