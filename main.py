from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import asyncio

from dotenv import load_dotenv
from os import getenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    commands = ""
    for i in COMMANDS:
        commands += f"/{i}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me!\nThere are my commands: \n{commands}")

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

COMMANDS = [
    'start',
    'im_user',
    'get_gid',
    'get_loc',
    'get_ctc',
    'get_doc',
    'get_id'
]

HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('im_user', im_user),
    CommandHandler('get_gid', get_gid),
    CommandHandler('get_loc', get_loc),
    CommandHandler('get_ctc', get_ctc),
    CommandHandler('get_doc', get_doc),

    CommandHandler('get_id', get_id)
]

# Funcion Principal
def main():
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)

    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    
    load_dotenv()
    main()