from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


async def get_doc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
    await context.bot.send_document(chat_id=update.effective_chat.id, document=open('test.txt', 'rb'), caption='Test Document')