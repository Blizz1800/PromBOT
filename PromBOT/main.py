from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler
from telegram.ext.filters import TEXT, COMMAND, PHOTO

from dotenv import load_dotenv
from os import getenv

from .db_init import db_init_update
from .commands import consts, start, code, start_handler, im_user, db_len, referrers, money_handler, cmd_handlers

code = ConversationHandler(
                entry_points=[CommandHandler('code', code.gen_msg)],
                states={
                    0: [MessageHandler(TEXT, code.gen_code)]
                },
                fallbacks=[lambda: print('No se encontró el código')],
            )

HANDLERS = [
    code,
    ConversationHandler(
        entry_points=[CommandHandler('start', start.start), MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
        states={
            0: [MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
            1: [MessageHandler(TEXT & (~COMMAND), referrers.refferers_handler)],
            2: [MessageHandler((TEXT | PHOTO) & (~COMMAND), money_handler.money_handler)],
        },
        fallbacks=[
            code
        ]
    ),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['SUB']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['CODE']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['ACCEPT']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['DENY']),
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