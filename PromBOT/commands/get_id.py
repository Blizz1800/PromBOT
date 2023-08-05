from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


async def get_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'```{update.effective_chat.id}```', parse_mode='MarkdownV2')