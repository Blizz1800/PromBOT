from telegram import Update, ChatMemberBanned, ChatMemberLeft, ReplyKeyboardMarkup, error
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from . import DB, consts, control

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, start_msg=True) -> None:
    if update.effective_chat.id < 0:
        return
    try :
        await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    except error.Forbidden as e:
        print(e)
        print(update.effective_user)
    id = update.effective_chat.id
    name = consts.format_mk(update.effective_user.full_name)
    user = consts.format_mk(f"@{update.effective_chat.username}")
    tk_b_start = 0

    referrer = None     # Referidor [REFERIDO PADRE!!]
    _self = DB['users'].find_one({"t_id": id})
    if context.args is not None:
        if len(context.args) != 0:
            referrer = int(context.args[0])     # Vemos quien esta refiriendo
            if _self is None:   # Si aun no existimos en la DB
                referral = DB['users'].find_one({"t_id": referrer})
                if referral is not None:
                    referir = True
                    for i in referral['referrals']:
                        if i == id:
                            await context.bot.send_message(chat_id=id, text=f"Ya has sido referido a este usuario")
                            referir = False
                            break
                    if referir:
                        DB['users'].update_one({"t_id": referrer}, {"$push": {'referrals': id}})
                        if referral['user'] is None:
                            username = referral['user'] 
                        else:
                            username = referral['name']                    
                        DB['users'].update_one({"t_id": referrer}, {"$inc": {'token_b': 1}})
                        reff = name
                        if user != "@None":
                            reff = user

                        await context.bot.send_message(referral['t_id'], text=f"Has referido a {reff}, has ganado *+1 {consts.TOKEN_NAME[1]}*", parse_mode=consts.MARKDOWN)
                        await context.bot.send_message(chat_id=id, text=f"Hola {update.effective_chat.first_name}! has sido invitado por {referral['user']}, obtendras 2 {consts.TOKEN_NAME[1]} cuando hayas sido activado!")
                        # tk_b_start = 2
                else:
                    await context.bot.send_message(chat_id=id, text=f"No existe un usuario con este ID({context.args[0]})")
            else:   # Si EXISTIMOS en la DB
                await context.bot.send_message(chat_id=id, text="Usted ya es usuario del bot!")
                
              
                

    group_id = consts.GROUP_ID
    user_in_chat = await context.bot.get_chat_member(group_id, update.effective_user.id)

    codes = DB['codes'].find({})
    code_l = []
    if codes is not None:
        for c in codes:
            code_l.append(c['code'])

    users_t = DB['users']
    if (users_t.find_one({"t_id": id}) is None):
        users_t.insert_one(
            {
                "t_id": id,
                "name": name,
                "user": user,
                "inGroup": not isinstance(user_in_chat, (ChatMemberBanned, ChatMemberLeft)),
                "active": False,
                "mail": None,
                "phone": None,
                "referrer": referrer,   # Referido padre
                "referrals": [],
                'inviteds': {
                    'count': 0,
                    'users': []
                },
                "token_a": 0,
                "token_b": tk_b_start,
                "limit_b": 10,  # Limit Bottom
                "dA": 5,        # Delta A. (Variacion del aumento)
                "extractions": 0,
                "banned": False,
                "codes": code_l,
                "target": None,
                "rifa":{
                    "invitados": [],
                    "need_invited": 5,
                    "rifas_w": 0
                }
            }
        )
    

    commands = ""
    for i in consts.COMMANDS:
        commands += f"/{i}\n"
    
    if start_msg:
        # btns = [[consts.BTS['FOLLOWERS']],
        #     [name, consts.BTS['REFERIDOS']['KEY']],
        #     [consts.BTS['MONEY']['GET'], consts.BTS['MONEY']['POST']]]
        await control("START:1", update, context)
        # await context.bot.send_message(chat_id=id, text="", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
    return 0