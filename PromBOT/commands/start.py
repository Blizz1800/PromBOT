from telegram import Update, ChatMemberBanned, ChatMemberLeft, ReplyKeyboardMarkup
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from . import DB, consts

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, start_msg=True) -> None:

    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)
    id = update.effective_chat.id
    name = update.effective_chat.full_name
    user = f"@{update.effective_chat.username}"   

    referrer = None     # Referidor [REFERIDO PADRE!!]
    _self = DB['users'].find_one({"t_id": id})
    if context.args is not None:
        if long(context.args) != 0:
            referrer = int(context.args[0])     # Vemos quien esta refiriendo
            if _self is None:   # Si aun no existimos en la DB
                referral = DB['users'].find_one({"t_id": referrer})
                if referral is not None:
                    referir = True
                    for i in referral['referrals']:
                        if i == id:
                            await context.bot.send_message(chat_id=id, text=f"You have already referred to this one")
                            referir = False
                            break
                    if referir:
                        DB['users'].update_one({"t_id": referrer}, {"$push": {'referrals': id}})
                        if referral['user'] is None:
                            username = referral['user'] 
                        else:
                            username = referral['name']                    
                        DB['users'].update_one({"t_id": referrer}, {"$inc": {'token_b': 1}})
                        await context.bot.send_message(referral['t_id'], text=f"Has referido a @{update.effective_user.username}")
                        await context.bot.send_message(chat_id=id, text=f"Hello {update.effective_user.first_name}! you have invited by {referral['user']}")
                else:
                    await context.bot.send_message(chat_id=id, text=f"No user found with this id ({context.args[0]})")
            else:   # Si EXISTIMOS en la DB
                await context.bot.send_message(chat_id=id, text="Usted ya es usuario del bot!")
                # referral = DB['users'].find_one({"t_id": _self['referrer']})    # Sacamos 
                # if _self['referrer'] is not None:
                #     if referral['user'] is not None:
                #         await context.bot.send_message(id, text=f"You have already referred to {referral['user']}")
                #     else:
                #         await context.bot.send_message(id, text=f"You have already referred to {referral['name']} ({referral['t_id']})")
                # else:
                #     DB['users'].update_one({"t_id": id}, {"$set": {'referrer': referrer}})
                #     DB['users'].update_one({"t_id": referrer}, {"$push": {'referrals': id}})
                #     DB['users'].update_one({"t_id": referrer}, {"$inc": {'token_b': 1}})

                #     await context.bot.send_message(referrer, text=f"Has referido a @{update.effective_user.username}\ntoken_b Now: *{referral['token_b']}*", parse_mode='Markdown')
                #     await context.bot.send_message(chat_id=id, text=f"Hello {update.effective_user.first_name}! you have invited by {referral['user']}")
              
                

    group_id = '@test_blizzbot_group'
    user_in_chat = await context.bot.get_chat_member(group_id, id)

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
                "referrer": referrer,
                "referrals": [],
                "token_a": 0,
                "token_b": 0,
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
        btns = [[consts.BTS['FOLLOWERS']],
            [name, consts.BTS['REFERIDOS']['KEY']],
            [consts.BTS['MONEY']['GET'], consts.BTS['MONEY']['POST']]]
        await context.bot.send_message(chat_id=id, text=f"I'm a bot, please talk to me!\nThere are my commands: \n{commands}", reply_markup=ReplyKeyboardMarkup(btns, resize_keyboard=True))
    return 0