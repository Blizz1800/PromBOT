from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from . import DB, consts

async def db_len(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    if update.effective_message.chat.id not in consts.ADMINS:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Usted no es *BOT\\_ADMIN*", parse_mode='MarkdownV2')
        return
    len_c = DB['users'].estimated_document_count()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Usuarios del Bot: ```{len_c}```', parse_mode='MarkdownV2')