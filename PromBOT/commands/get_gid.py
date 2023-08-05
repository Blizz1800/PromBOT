from telegram import Update, ChatMemberBanned, ChatMemberLeft
from telegram.constants import ChatAction
from telegram.ext import ContextTypes


async def get_gid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    group_id = '@test_blizzbot_group'
    group_i_id = await context.bot.getChat(group_id)
    group_i_id = group_i_id.id
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f'```{group_i_id}```', parse_mode='MarkdownV2')