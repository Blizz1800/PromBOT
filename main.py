from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import asyncio

from dotenv import load_dotenv
from os import getenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

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

HANDLERS = [
    CommandHandler('start', start),
    CommandHandler('im_user', im_user),
    CommandHandler('get_gid', get_gid),
    CommandHandler('get_id', get_id)
]

# Funcion Principal
def main():
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)
    # for i in HANDLERS:
    #     print(f'{i.commands} added')
    #     app.add_handler(i)

    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    
    load_dotenv()
    main()