from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram.ext.filters import TEXT, COMMAND

from dotenv import load_dotenv
from os import getenv

from .commands import consts, start, code, start_handler, im_user, db_len, referrers, money_handler 

HANDLERS = [
    ConversationHandler(
        entry_points=[CommandHandler('start', start.start), CommandHandler('code', code.gen_msg), MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
        states={
            0: [MessageHandler(TEXT, start_handler.start_handler)],
            1: [MessageHandler(TEXT, referrers.refferers_handler)],
            2: [MessageHandler(TEXT, money_handler.money_handler)],
            100: [MessageHandler(TEXT, code.gen_code)]

        },
        fallbacks=[]
    ),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CommandHandler('im_user', im_user.im_user),
    CommandHandler('db_len', db_len.db_len),
    
]

# Funcion Principal
def main():
    load_dotenv()
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)
    db_init_update()
    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    main()