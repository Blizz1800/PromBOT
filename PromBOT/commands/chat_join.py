from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Bot, Chat
from telegram.ext import ContextTypes
from pprint import pprint

async def new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = update.message.new_chat_members
    
    kb = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text="🥵...Ir al privado sabroso...🤤", url=f"{context.bot.link}")
        ]]
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hola {USER}, bienvenido! Pasate por mi privado si quieres hacer un dinerito extra ;)\n\n*ES GRATIS!* :D".format(USER=update.effective_user.full_name), parse_mode="Markdown", reply_markup=kb)