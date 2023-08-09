from telegram.constants import ChatAction
from telegram import ReplyKeyboardMarkup
from PromBOT.commands.consts import BTS

async def get_referidos(update, context, DB):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    bts = [
        [BTS['FOLLOWERS']],
        [BTS['INFO'], BTS['REFERIDOS']],
        [BTS['MONEY']['WITHRAW'], BTS['MONEY']['EARN']]
    ]
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Encantado! Que clase de informacion necesita?", reply_markup=ReplyKeyboardMarkup(bts, resize_keyboard=True))

async def get_referidosV2(update, context, DB):
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    my_id = update.effective_user.id
    me = DB['users'].find_one({'t_id': my_id})
    reffs = me['referrals']
    result = []
    for i in reffs:
        R = DB['users'].find_one({'t_id': i})
        string = f"[`{R['t_id']}`] {R['name']}"
        if R['user'] is not None:
            string += f" \({R['user']}\)"
        result.append(string)
    if len(result) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="No se han referido a ningún usuario.")
    else:
        refs = "\n".join(result)
        resp = f"Usted a referido a:\n\n{refs}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=resp, parse_mode="MarkdownV2")