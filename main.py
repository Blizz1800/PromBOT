from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

import asyncio

from dotenv import load_dotenv
from os import getenv

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    print('start called!!')
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

HANDLERS = [
    CommandHandler('start', start),
]

# Funcion Principal
def main():
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    for i in HANDLERS:
        print(f'{i.callback} added')
    
    app.add_handler(CommandHandler('start', start))

    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    
    load_dotenv()
    main()