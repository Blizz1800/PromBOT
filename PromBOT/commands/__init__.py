from pymongo import MongoClient
from dotenv import load_dotenv
from os import getenv

import re
from .consts import get_msg

load_dotenv()

DB = MongoClient(getenv("MONGO_URI"))['vendermejor']

def get_db(db:str = "vendermejor"):
    return MongoClient(getenv("MONGO_URI"))[db]

async def control(key, update, context, ret=0):
    m = get_msg(key, user=update.effective_chat.full_name)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'], parse_mode=m['MARKDOWN'], reply_markup=m['BTN'])
    return ret

def validate(string: str) -> int:
    string = string.encode('utf-8')
    res = re.match(b"(.*\d{4}.*){4}", string)
    if res:
        return 0
    res = re.match(b"\+\d{1,3}(.*\d.*){4,16}", string)
    if res:
        return 1
    return -1