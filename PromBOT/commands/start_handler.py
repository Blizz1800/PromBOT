from telegram.ext import ContextTypes, ConversationHandler
from telegram import ChatInviteLink, Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ChatMemberLeft, ChatMemberBanned

from .consts import BTS, TOKEN_NAME, get_msg
from . import DB, cmd_handlers, code, start

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text

    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, update.effective_user.id)
    inGroup = not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft))
    DB['users'].update_one({'t_id': update.effective_user.id}, {'$set': {'inGroup': inGroup, 'active': inGroup}})


    name = DB['users'].find_one({'t_id': update.effective_user.id})
    if name is not None:
        if name['banned']:
            await context.bot.send_message(chat_id=update.effective_user.id, text="Tu has sido baneado, x tanto no puedes usar este servicio nunca mas\nPara mas dudas contactar los administradores", reply_markup=ReplyKeyboardRemove())
            return -1
        name = name['name']
    else:
        await start.start(update=update, context=context, start_msg=False)
        name = DB['users'].find_one({'t_id': update.effective_user.id})['name']

    if msg == name:
        return await cmd_handlers.get_info(update, context) # 0
    elif msg == BTS['REFERIDOS']['KEY']:
        return await cmd_handlers.get_referidos(update, context) # 1
    elif msg == BTS['FOLLOWERS']:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    elif msg == BTS['MONEY']['GET']:
        return await cmd_handlers.money.extraer(update=update, context=context) # 4 
    elif msg == BTS['MONEY']['POST']:
        return await cmd_handlers.money.ganar(update=update, context=context) # 2
    elif msg == BTS['RIFAS']:
        # return await cmd_handlers.money.ganar(update=update, context=context) # 3
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    else:
        p = get_msg('START', user=update.effective_user.full_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se reconoce su entrada", reply_markup=p['BTN'], parse_mode=p['MARKDOWN'])
    return 0
        
async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()
    
    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, query.from_user.id)

    # link_doc = DB['links'].find_one({'t_id': query.from_user.id})

    # if link_doc is None:
    #     link:ChatInviteLink = await context.bot.create_chat_invite_link(group_id, name=f"user:{update.effective_chat.id}", creates_join_request=True)
    #     DB['links'].insert_one(link.to_dict(True))
    #     link = link.invite_link
    # else:
    #     link = link_doc['link']


    # DB['users'].update_one({'t_id': query.from_user.id}, {'$set': {'inGroup': not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft))}})
    # if DB['users'].find_one({'t_id': update.effective_user.id})['inGroup'] and link_doc['invited'] >= 5:
    #     await context.bot.send_message(chat_id=query.from_user.id, text="Has sido activado!")
    #     DB['users'].update_one({'t_id': query.from_user.id}, {'$set': {"active": True}})
    #     return

    kb = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text=BTS['INVITE'], callback_data=f"{BTS['INVITE']}:5")
        ]]
    )

    await query.edit_message_text(text=f"Usted debe ingresar al grupo {group_id} e invitar {5} usuarios precionando este boton", reply_markup=kb)

async def share_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    btn, count = tuple(data.split(':')) 
    count = int(count) -1 


    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, query.from_user.id)
    DB['users'].update_one({'t_id': query.from_user.id}, {'$set': {'inGroup': not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft))}})

    if count <= 0:
        await query.edit_message_text(text="Has sido activado!")
        DB['users'].update_one({'t_id': query.from_user.id}, {'$set': {"active": True}})
        return

    kb = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text=BTS['INVITE'], callback_data=f"{BTS['INVITE']}:{count}")
        ]]
    )
    

    await query.edit_message_text(text=f"Usted debe ingresar al grupo {group_id} e invitar {count} usuarios precionando este boton", reply_markup=kb)
