from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ConversationHandler, ChatMemberHandler, PicklePersistence
from telegram.ext.filters import TEXT, COMMAND, PHOTO, Regex
from telegram import Update
from dotenv import load_dotenv
from os import getenv

from .db_init import db_init_update
from .commands import consts, start, pagos, reglas, code, start_handler, im_user, db_len, referrers, money_handler, cmd_handlers, chat_join, rifa, spam

from warnings import filterwarnings
from telegram.warnings import PTBUserWarning

filterwarnings(action="ignore", message=r".*CallbackQueryHandler", category=PTBUserWarning)

rules = CommandHandler('rules', reglas.get)
get_spam = CommandHandler('get_spam', spam.get)
get_pay = CommandHandler('get_pays', pagos.get_pays)
code = ConversationHandler(
                per_user=True,
                entry_points=[CommandHandler('code', code.gen_msg)],
                states={
                    0: [MessageHandler(TEXT | COMMAND, code.gen_code)]
                },
                fallbacks=[],
            )
spam_h = ConversationHandler(
    per_user=True,
    entry_points=[CommandHandler('spam', spam.insert)],
    states={
        0: [MessageHandler(TEXT & (~COMMAND), spam.insert_2),],
        1: [MessageHandler(TEXT & (~COMMAND), spam.advice),],
        2: [MessageHandler(TEXT & (~COMMAND), spam.advice_send),],
    },
    fallbacks=[]
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
                    0: [MessageHandler(TEXT & (~COMMAND), rifa.base_handler)]
                },
                fallbacks=[],
                map_to_parent={
                    -1: 0
                }
            )]
        },
        fallbacks=[
            code,
            get_pay,
            rules,
            get_spam,
            spam_h
        ],
    )

async def all(u, c):
    query = u.callback_query
    print(query.data)


HANDLERS = [
    CallbackQueryHandler(all),
    ConversationHandler(
        entry_points=[CallbackQueryHandler(money_handler.tlgm_spam, pattern=consts.BTS['INLINE']['SPAM']),CallbackQueryHandler(money_handler.tlgm_bot, pattern=consts.BTS['INLINE']['BOT'])],
        states={
            0: [MessageHandler(PHOTO & (~TEXT & ~COMMAND), money_handler.get_photo), CommandHandler('end', money_handler.ig_end), CallbackQueryHandler(money_handler.tlgm_spam, pattern=consts.BTS['INLINE']['SPAM']),CallbackQueryHandler(money_handler.tlgm_bot, pattern=consts.BTS['INLINE']['BOT'])]
        },
        fallbacks=[],
        per_user=True,
    ),
    ConversationHandler(
        entry_points=[CallbackQueryHandler(money_handler.tlgm_bot, pattern=consts.BTS['INLINE']['BOT'])],
        states={
            0: [MessageHandler(PHOTO & (~TEXT & ~COMMAND), money_handler.get_photo), CommandHandler('end', money_handler.ig_end)]
        },
        fallbacks=[],
        per_user=True,
    ),
    ConversationHandler(
        entry_points=[CallbackQueryHandler(money_handler.ig_comments, pattern=consts.BTS['INLINE']['COMENT'])],
        states={
            0: [MessageHandler(PHOTO & (~TEXT & ~COMMAND), money_handler.get_photo), CommandHandler('end', money_handler.ig_end), CallbackQueryHandler(money_handler.ig_comments, pattern=consts.BTS['INLINE']['COMENT'])]
        },
        fallbacks=[],
        per_user=True,
    ),
    code,
    get_spam,
    spam_h,
    get_pay,
    rules,
    entry,
    ConversationHandler(
        entry_points=[CallbackQueryHandler(money_handler.aviso_pago, pattern=consts.BTS['INLINE']['PAGO'])],
        states={
            1: [MessageHandler((TEXT | PHOTO) & (~COMMAND), money_handler.envio)],
        },
        fallbacks=[],
        per_user=True,
    ),
    ChatMemberHandler(callback=chat_join.new_member, chat_member_types=ChatMemberHandler.CHAT_MEMBER),
    CallbackQueryHandler(start_handler.activate_handler, pattern=consts.BTS['INLINE']['ACTIVATE']),
    CallbackQueryHandler(start_handler.send_how_to, pattern=consts.BTS['INLINE']['SEND_PHOTO']),
    CallbackQueryHandler(start_handler.update_handler, pattern=consts.BTS['INLINE']['UPDATE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['SUB']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['CODE']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['REELS']),
    CallbackQueryHandler(money_handler.buttons, pattern=consts.BTS['INLINE']['FOLLOW']),
    CallbackQueryHandler(money_handler.admin_btn_v2, pattern=f"{consts.BTS['INLINE']['ACCEPT']}2"),
    CallbackQueryHandler(money_handler.admin_btn_v2, pattern=f"{consts.BTS['INLINE']['DENY']}2"),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['ACCEPT']),
    CallbackQueryHandler(money_handler.admin_btn, pattern=consts.BTS['INLINE']['DENY']),
    CallbackQueryHandler(spam.remove, pattern="rem"),
    CallbackQueryHandler(spam.prior, pattern="prior"),
    CallbackQueryHandler(pagos.get_more, pattern=consts.BTS['INLINE']['MORE']),
    CommandHandler('im_user', im_user.im_user),
    CommandHandler('db_len', db_len.db_len),
    
]

# Funcion Principal
def main():
    load_dotenv()
    persistence = PicklePersistence(filepath="data.bin")
    app = ApplicationBuilder().token(getenv('TOKEN')).persistence(persistence=persistence).build()
    app.add_handlers(HANDLERS)
    db_init_update()
    print('Bot Running!')
    app.run_polling(allowed_updates=Update.ALL_TYPES)
    


# Buenas Practicas
if __name__ == '__main__':
    main()