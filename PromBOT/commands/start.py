from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from commands import consts

from . import DB

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    
    id = update.effective_chat.id
    name = update.effective_chat.full_name
    user = f"@{update.effective_chat.username}"    

    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, id)

    users_t = DB['vendermejor']['users']
    if (users_t.find_one({"t_id": id}) is None):
        users_t.insert_one(
            {
                "t_id": id,
                "name": name,
                "user": user,
                "inGroup": not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)),
                "active": False,
                "mail": None,
                "phone": None
            }
        )

    commands = ""
    for i in consts.COMMANDS:
        commands += f"/{i}\n"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"I'm a bot, please talk to me!\nThere are my commands: \n{commands}")