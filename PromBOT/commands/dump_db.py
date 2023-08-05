from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from commands import consts

async def dump_db(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_chat.id in consts.ADMINS:
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="En mantenimiento")
        return
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Usted no es *BOT\\_ADMIN*", parse_mode='MarkdownV2')