from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from PromBOT.commands.consts import TOKEN_NAME, BTS
from PromBOT.commands import DB

async def get_info(update, context):
    me = DB['users'].find_one({'t_id': update.effective_chat.id})
    resp = f"*{me['name']}*\n\n_En el grupo_: "
    line_btn = [[]]
    if me['inGroup']:
        resp += "*Si*\n"
    else:
        resp += "*No*\n"
        line_btn[0].append(InlineKeyboardButton(BTS['INLINE']['ACTIVATE'], callback_data=BTS['INLINE']['ACTIVATE']))   # Agregar un boton para entrar al grupo
    if me['active']:
        resp += "_Activo_: *Si*\n" 
    else:
        resp += "_Activo_: *No*\n" 
    if me['mail']:
        resp += f"_Correo_: {me['mail']}\n"
    if me['phone']:
        resp += f"_Telefono_: {me['phone']}\n"
    if me['referrer']:
        tmp = DB['users'].find_one({'t_id': me['referrer']})
        resp += f"_Anfitrion_: [{tmp['name']}]\(tg://user?id\={me['referrer']}\)\n"
    tk = me['token_b']
    if tk > 1:
        resp += f"_{TOKEN_NAME[1]}_: `{tk}`\n"
    else:
        resp += f"_{TOKEN_NAME[0]}_: `{tk}`\n"
    
    if len(line_btn) > 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="MarkdownV2", text=resp, reply_markup=InlineKeyboardMarkup(line_btn))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="MarkdownV2", text=resp)
    return 0