from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

from dotenv import load_dotenv
from os import getenv

from datetime import datetime

DB_NAME = "db_users"
CACHE_NAME = "db_cache"


BLIZZ = 1287864142

ADMINS = [
    BLIZZ
]

def store_db(id, *params) -> None:
    insert = True

    db = open(f"./{DB_NAME}.txt", 'w+')

    for i in db.readlines():
        if i == "\n":
            break
        if i.split("\0")[0] == str(id):
            insert = False
            break

    if insert:

        cache = open(f"./{CACHE_NAME}.txt", 'w+')
        try:
            maxusers = int(cache.readline())
        except:
            maxusers = 0
        maxusers += 1
        cache.write(str(maxusers))
        cache.close()

        db.close()
        db = open(f"./{DB_NAME}.txt", 'a')
        db_entry = "f{id}"
        for i in params:
            if i != params[-1]:
                db_entry += "\0"
            db_entry += f"{i}"
        if (db.writable):
            db.write(f"{db_entry}\n")
        else:
            db.close()
            return db_entry
    db.close()
    return

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    
    id = update.effective_chat.id
    name = f"{update.effective_chat.first_name} {update.effective_chat.last_name}"
    user = f"@{update.effective_chat.username}"

    msg = store_db(id, name, user)
    if msg is not None:
        await context.bot.send_message(chat_id=BLIZZ, text=f"El archivo db.txt no se puede escribir, estos son los datos del usuario: \n{msg}")


    commands = ""
    for i in COMMANDS:
        commands += f"/{i}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me!\nThere are my commands: \n{commands}")

async def dump_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id in ADMINS:
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(f"./{DB_NAME}.txt", 'rb'), filename="db.txt", caption=f"{datetime.utcnow().strftime('%d-%m-%Y %H:%M:%S')}")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Usted no es *BOT\\_ADMIN*", parse_mode='MarkdownV2')
    

async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'```{update.effective_chat.id}```', parse_mode='MarkdownV2')

async def get_gid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    group_id = '@test_blizzbot_group'
    group_i_id = await context.bot.getChat(group_id)
    group_i_id = group_i_id.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'```{group_i_id}```', parse_mode='MarkdownV2')

async def im_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    user_id = update.effective_chat.id
    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, user_id)
    
    if not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)) :
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello {user_in_chat.user.first_name}, you are welcomed!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello {user_in_chat.user.first_name}, you aren\'t welcomed!\nPlease enter to {group_id}')

async def get_loc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.FIND_LOCATION)
    # 23.046640611793258, -81.57829721120095
    await context.bot.send_location(chat_id=update.effective_chat.id, latitude=23.046640611793258, longitude= -81.57829721120095)

async def get_ctc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
    await context.bot.send_contact(chat_id=update.effective_chat.id, phone_number='+53 53013028', first_name='Blizz', last_name='Softword')

async def get_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open('test.txt', 'rb'), caption='Test Document')

async def db_len(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    if update.effective_message.chat.id not in ADMINS:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usted no es *BOT\\_ADMIN*", parse_mode='MarkdownV2')
        return
    len_c = open(f"./{CACHE_NAME}.txt", 'r').readline()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Usuarios del Bot: ```{len_c}```', parse_mode='MarkdownV2')

COMMANDS = [
    'start',
    'im_user',
    'get_gid',
    'get_loc',
    'get_ctc',
    'get_doc',
    'dump_db',
    'db_len',
    'get_id'
]

HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('im_user', im_user),
    CommandHandler('get_gid', get_gid),
    CommandHandler('get_loc', get_loc),
    CommandHandler('get_ctc', get_ctc),
    CommandHandler('get_doc', get_doc),
    CommandHandler('dump_db', dump_db),
    CommandHandler('db_len', db_len),
    CommandHandler('get_id', get_id)
]


# Funcion Principal
def main():
    load_dotenv()
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)

    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    main()