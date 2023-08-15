from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, ChatJoinRequestHandler
from telegram.ext.filters import TEXT, COMMAND, PHOTO, StatusUpdate

from dotenv import load_dotenv
from os import getenv

from .db_init import db_init_update
from .commands import consts, start, code, start_handler, im_user, db_len, referrers, money_handler, cmd_handlers, chat_join

code = ConversationHandler(
                entry_points=[CommandHandler('code', code.gen_msg)],
                states={
                    0: [MessageHandler(TEXT, code.gen_code)]
                },
                fallbacks=[lambda: print('No se encontró el código')],
            )

entry = ConversationHandler(
        entry_points=[CommandHandler('start', start.start), MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
        states={
            0: [MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
            1: [MessageHandler(TEXT & (~COMMAND), referrers.refferers_handler)],
            2: [MessageHandler((TEXT | PHOTO) & (~COMMAND), money_handler.money_handler)],
            4: [
                ConversationHandler(
                    entry_points=[MessageHandler(TEXT & (~COMMAND), money_handler.extract_handler)],
                    states={
                        0: [MessageHandler(TEXT & (~COMMAND), money_handler.extract)],
                        1: [MessageHandler(TEXT & (~COMMAND), money_handler.target_handler)],
                        2: [MessageHandler(TEXT & (~COMMAND), money_handler.extract_handler)],
                    },
                    fallbacks=[],
                    map_to_parent={
                        -1: 0
                    })
                ]
        },
        fallbacks=[
            code
        ]
    )

HANDLERS = [
    code,
    entry,
    MessageHandler(StatusUpdate.NEW_CHAT_MEMBERS, chat_join.new_member),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['SUB']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['CODE']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['ACCEPT']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['DENY']),
    CallbackQueryHandler(start_handler.share_handler, pattern=consts.BTS['INVITE']),
    CommandHandler('im_user', im_user.im_user),
    CommandHandler('db_len', db_len.db_len),
    
]

# Funcion Principal
def main():
    load_dotenv()
    app = ApplicationBuilder().token(getenv('TOKEN')).build()
    app.add_handlers(HANDLERS)
    app.bot_data['start_ch'] = entry
    db_init_update()
    print('Bot Running!')
    app.run_polling()
    


# Buenas Practicas
if __name__ == '__main__':
    main()