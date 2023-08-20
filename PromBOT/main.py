from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, ChatJoinRequestHandler
from telegram.ext.filters import TEXT, COMMAND, PHOTO, StatusUpdate

from dotenv import load_dotenv
from os import getenv

from .db_init import db_init_update
from .commands import consts, start, pagos, code, start_handler, im_user, db_len, referrers, money_handler, cmd_handlers, chat_join, rifa

get_pay = CommandHandler('get_pays', pagos.get_pays)
code = ConversationHandler(
    per_user=True,
                entry_points=[CommandHandler('code', code.gen_msg)],
                states={
                    0: [MessageHandler(TEXT & COMMAND, code.gen_code)]
                },
                fallbacks=[lambda: print('No se encontró el código')],
            )

entry = ConversationHandler(
    per_user=True,
        entry_points=[CommandHandler('start', start.start), MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
        states={
            0: [MessageHandler(TEXT & (~COMMAND), start_handler.start_handler)],
            1: [MessageHandler(TEXT & (~COMMAND), referrers.refferers_handler)],
            2: [MessageHandler((TEXT | PHOTO) & (~COMMAND), money_handler.money_handler)],
            4: [ConversationHandler(
                    entry_points=[MessageHandler(TEXT & (~COMMAND), money_handler.extract_handler)],
                    states={
                        0: [MessageHandler(TEXT & (~COMMAND), money_handler.extract)],
                        1: [MessageHandler(TEXT & (~COMMAND), money_handler.target_handler)],
                        2: [MessageHandler(TEXT & (~COMMAND), money_handler.extract_handler)],
                    },
                    fallbacks=[],
                    map_to_parent={
                        -1: 0,
                    })
                ],
            5: [ConversationHandler(
                entry_points=[MessageHandler(TEXT & (~COMMAND), rifa.base_handler)],
                states={
                    0: [MessageHandler(TEXT & (~COMMAND), rifa.get_info)]
                },
                fallbacks=[],
                map_to_parent={
                    -1: 0
                }
            )]
        },
        fallbacks=[
            code,
            get_pay
        ],
    )

HANDLERS = [
    code,
    get_pay,
    entry,
    ConversationHandler(
        entry_points=[CallbackQueryHandler(money_handler.aviso_pago, pattern=consts.BTS['INLINE']['PAGO'])],
        states={
            1: [MessageHandler((TEXT | PHOTO) & (~COMMAND), money_handler.envio)],
        },
        fallbacks=[],
        per_user=True
    ),
    MessageHandler(StatusUpdate.NEW_CHAT_MEMBERS, chat_join.new_member),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['SUB']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['CODE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['COMENT']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['REELS']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['FOLLOW']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['ACCEPT']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['DENY']),
    CallbackQueryHandler(start_handler.share_handler, pattern=consts.BTS['INVITE']),
    CallbackQueryHandler(pagos.get_more, pattern=consts.BTS['INLINE']['MORE']),
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