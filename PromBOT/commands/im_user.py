from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from .consts import GROUP_ID

async def im_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    user_id = update.effective_chat.id
    group_id = GROUP_ID
    user_in_chat = await context.bot.get_chat_member(group_id, user_id)
    
    if not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)) :
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello {user_in_chat.user.first_name}, you are welcomed!')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Hello {user_in_chat.user.first_name}, you aren\'t welcomed!\nPlease enter to {group_id}')