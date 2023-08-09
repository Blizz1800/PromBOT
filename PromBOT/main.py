from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram.ext.filters import TEXT

from dotenv import load_dotenv
from os import getenv

from .commands import consts, start, start_handler, im_user, db_len

HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler('start', start.start)],
        states={
            0: [MessageHandler(TEXT, start_handler.start_handler)]
        },
        fallbacks=[]
    ),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CommandHandler('im_user', im_user.im_user),
    CommandHandler('db_len', db_len.db_len)
]

# Funcion Principal
def main():
    load_dotenv()
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)

    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    main()