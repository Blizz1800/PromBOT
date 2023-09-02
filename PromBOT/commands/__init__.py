from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

from telegram import Update, constants, error
from telegram.ext import ContextTypes

import re
from .consts import get_msg, ADMINS, MARKDOWN

load_dotenv()

DB = MongoClient(getenv("MONGO_URI"))['vendermejor']

def get_db(db:str = "vendermejor"):
    return MongoClient(getenv("MONGO_URI"))[db]

async def control(key: str, update: Update, context: ContextTypes.DEFAULT_TYPE, ret=0, *args, **kargs):
    m = get_msg(key, user=update.effective_user.full_name)
    mr = m['MARKDOWN']
    r = m['BTN']
    # print("\t\tControl: ", m)
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'].format(*args, **kargs), parse_mode=mr, reply_markup=r)
        return ret
    except error.Forbidden as e:
        for i in ADMINS:
            await context.bot.send_message(chat_id=i, parse_mode=MARKDOWN, text=f"No se pudo hacer llegar el mensaje\n```{m['MSG']}``` al usuario con id `{update.effective_chat.id}` ({update.effective_user.full_name})\n\nMotivo: \"```{e}```\"")
        return ret


def validate(string: str) -> int:
    string = string.encode('utf-8')
    res = re.match(b"(\s*\d{4}\s*){4}", string)
    if res:
        return 0
    res = re.match(b"(\+\d{1,3})?(\s*\d\s*){4,16}", string)
    if res:
        return 1
    return -1