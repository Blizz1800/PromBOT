from telegram import Update, InlineKeyboardMarkup, ChatMemberUpdated, ChatMember, constants, ChatInviteLink
from telegram.ext import ContextTypes
# from pprint import pprint

from . import DB
from .consts import TOKEN_NAME, MESSAGES

def get_status_change(update: ChatMemberUpdated):
    status = update.difference()
    status = status.get('status')
    old_is_member, new_is_member = update.difference().get("is_member", (None, None))

    if status is None:
        return None
    
    old_status, new_status = status

    was_member = old_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (old_status == ChatMember.RESTRICTED and old_is_member is True)

    is_member = new_status in [
        ChatMember.MEMBER,
        ChatMember.OWNER,
        ChatMember.ADMINISTRATOR,
    ] or (new_status == ChatMember.RESTRICTED and new_is_member is True)

    return was_member, is_member


async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    m = MESSAGES['GROUP']
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=constants.ChatAction.TYPING)
    result = get_status_change(update.chat_member)
    if result is None:
        return
    
    was_member, is_member = result

    cause = update.chat_member.from_user
    new_user = update.chat_member.new_chat_member.user
    print(f"{new_user.full_name} was enter by {update.chat_member.invite_link}")

    if not was_member and is_member:
        kb = InlineKeyboardMarkup(m['BTN'])
        incoming = new_user.full_name
        if new_user.username:
            incoming = f'@{new_user.username}'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][0].format(USER=incoming), parse_mode="Markdown", reply_markup=kb)
        if not cause.id == new_user.id:
            DB['users'].update_one(
                {'t_id': cause.id},
                {
                    '$inc': 
                        {'inviteds.count': 1},
                    '$push':
                        {'users': new_user.id}
                }
            )
            await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][2].format(INVITER=update.chat_member.from_user.full_name, USER=incoming))

    elif was_member and not is_member:
        outgoing = new_user.full_name
        if new_user.username:
            outgoing = f'@{new_user.username}'
        await context.bot.send_message(chat_id=update.effective_chat.id, text=m['MSG'][1].format(USER=outgoing))
    