from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


async def get_loc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.FIND_LOCATION)
    # 23.046640611793258, -81.57829721120095
    await context.bot.send_location(chat_id=update.effective_chat.id, latitude=23.046640611793258, longitude= -81.57829721120095)