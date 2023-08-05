from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


async def get_ctc(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.UPLOAD_DOCUMENT)
    await context.bot.send_contact(chat_id=update.effective_chat.id, phone_number='+53 53013028', first_name='Blizz', last_name='Softword')