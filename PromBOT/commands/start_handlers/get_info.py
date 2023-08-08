from telegram.ext import ContextTypes, ConversationHandler
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

async def get_info(update, context, DB):
    me = DB['users'].find_one({'t_id': update.effective_chat.id})
    resp = f"**{me['name']}**\n\n__En el grupo__: "
    if me['inGroup']:
        resp += "**Si**\n"
    else:
        resp += "**No**\n"
        line_btn.append(InlineKeyboardButton(BTS['ACTIVATE']), callback_data=BTS['ACTIVATE'])   # Agregar un boton para entrar al grupo
    resp += f"__Activo__: {me['active']}\n" 
    if me['mail']:
        resp += f"__Correo__: {me['mail']}\n"
    if me['phone']:
        resp += f"__Telefono__: {me['phone']}\n"
    if me['referrer']:
        tmp = DB['users'].find_one({'t_id': me['referrer']})
        resp += f"__Anfitrion__: ({tmp['name']})[tg://user?id={me['referrer']}]\n"
    tk = me['tokens']
    if tk > 1:
        resp += f"__{TOKEN_NAME[1]}__: {tk}\n"
    else:
        resp += f"__{TOKEN_NAME[0]}__: {tk}\n"
    
    if len(line_btn) > 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="MarkdownV2", text=resp, reply_markup=InlineKeyboardMarkup(line_btn))
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, parse_mode="MarkdownV2", text=resp)