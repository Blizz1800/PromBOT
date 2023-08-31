from telegram.ext import ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, ChatMemberLeft, ChatMemberBanned, constants

from . import analytics

from .consts import BTS, TOKEN_NAME, get_msg
from . import DB, cmd_handlers, code, start, control

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text
    name = DB['users'].find_one({'t_id': update.effective_chat.id})
    # print(f"{name['name']}\t{name['t_id']}")

    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, update.effective_user.id)
    inGroup = not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft))


    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    if name is not None:
        DB['users'].update_one({'t_id': update.effective_chat.id}, {'$set': {'inGroup': inGroup}})
        if name['banned']:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Tu has sido baneado, x tanto no puedes usar este servicio nunca mas\nPara mas dudas contactar los administradores", reply_markup=ReplyKeyboardRemove())
            return -1
        name = name['name']
    else:
        await start.start(update=update, context=context, start_msg=False)
        name = DB['users'].find_one({'t_id': update.effective_chat.id})['name']

    if msg == name:
        analytics.button_press('INFO', update.effective_chat.id)
        return await cmd_handlers.get_info(update, context) # 0
    elif msg == BTS['REFERIDOS']['KEY']:
        analytics.button_press(BTS['REFERIDOS']['KEY'], update.effective_chat.id)
        return await cmd_handlers.get_referidos(update, context) # 1
    elif msg == BTS['FOLLOWERS']:
        analytics.button_press(BTS['FOLLOWERS'], update.effective_chat.id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Under Construction!")
    elif msg == BTS['MONEY']['GET']:
        analytics.button_press(BTS['MONEY']['GET'], update.effective_chat.id)
        return await cmd_handlers.money.extraer(update=update, context=context) # 4 
    elif msg == BTS['MONEY']['POST']:
        analytics.button_press(BTS['MONEY']['POST'], update.effective_chat.id)
        return await cmd_handlers.money.ganar(update=update, context=context) # 2
    elif msg == BTS['RIFAS']['KEY']:
        analytics.button_press(BTS['RIFAS']['KEY'], update.effective_chat.id)
        return await control('RIFAS', update, context, 5)
    elif msg == BTS['REGLAS']:
        analytics.button_press(BTS['REGLAS'], update.effective_chat.id)
        return await control('REGLAS', update, context)
    else:
        await control('START:3', update, context)
    return 0

async def update_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    await context.bot.send_chat_action(update.effective_chat.id, constants.ChatAction.TYPING)
    count = DB['users'].find_one({'t_id': query.from_user.id})['inviteds']['count'] 
    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, query.from_user.id)
    analytics.button_press(BTS['INLINE']['UPDATE'], update.effective_chat.id, True)

    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton(BTS['INLINE']['UPDATE'], callback_data=BTS['INLINE']['UPDATE'])]]
    )
    

    if not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)):
        if  count >= 5:
            me = DB['users'].find_one({'t_id': query.from_user.id})
            many = 0
            if me['referrer']:
                many = 2
                DB['users'].update_one(
                    {'t_id': me['referrer']},
                    {
                        '$inc': {
                            'token_b': 1
                        }
                    }
                )
                analytics.earn_tk(analytics.TK_RED.REFERIDOS, me['referrer'], 1, analytics.TK.B)
                await context.bot.send_message(chat_id=me['referrer'], text="Su referido {USER} ha sido activado, usted ha ganado 1 {TOKEN}".format(USER=me['name'], TOKEN=TOKEN_NAME[1]))
            DB['users'].update_one(
                {'t_id': query.from_user.id},
                {
                    '$set': {
                        'inGroup': not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)),
                        'active': not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)) and count >= 5
                    },
                    '$inc': {
                        'token_b': many
                    }
                    
                }
            )
            analytics.earn_tk(analytics.TK_RED.REFERIDOS, query.from_user.id, 1, analytics.TK.B)
            
            if many > 0:
                bono = f"\n\n😱Ha recibido un bono de: {many} {TOKEN_NAME[1]}💸"
            else:
                bono = ""
            txt = "🎊Usted ya es un usuario activo🎉\nDisfrute de su subscripcion😊{BONO}".format(BONO=bono)
            kb = InlineKeyboardMarkup([[]])
        else:
            txt = "Usted debe agregar aun {MANY} mas usuarios al grupo {ID}, ha agregado {COUNT}/5"
    else:
        txt = "Usted no es miembro del grupo {ID}, por favor, ingresar al grupo y permanecer alli, e invitar {MANY} usuarios mas."
    try:
        await query.edit_message_text(reply_markup=kb, text=txt.format(ID=group_id, MANY=5-count, COUNT=count))
    except Exception as e:
        print(e)
        await query.answer()


async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    await query.answer()

    count = DB['users'].find_one({'t_id': query.from_user.id})['inviteds']['count'] 
    group_id = '@test_blizzbot_group'

    analytics.button_press(BTS['INLINE']['ACTIVATE'], update.effective_chat.id, True)

    kb = InlineKeyboardMarkup(
        [[InlineKeyboardButton(BTS['INLINE']['UPDATE'], callback_data=BTS['INLINE']['UPDATE'])]]
    )

    txt = "Usted debe ingresar al grupo📥 {ID} y agregar {MANY} suarios 👤más \n\n👤Usuarios agregados: {COUNT}/5"
    try:
        await query.edit_message_text(reply_markup=kb, text=txt.format(ID=group_id, MANY=5-count, COUNT=count))
    except Exception as e:
        # print(e)
        await query.answer()

    
