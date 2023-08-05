from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

async def referir(update: Update, context: ContextTypes) -> None:
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    bot = await context.bot.get_me()
    link = f"https://t.me/{bot.username}?start={update.effective_user.id}"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Enviale este link a tus amigos para referirlos:\n\n{link}")