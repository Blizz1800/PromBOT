from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler

from dotenv import load_dotenv
from os import getenv

from commands import start, im_user, get_gid, get_loc, get_ctc, get_doc, db_len, get_id, referir, referidos

HANDLERS = [
    CommandHandler('start', start.start),
    CommandHandler('referir', referir.referir),
    CommandHandler('referidos', referidos.referidos),
    CommandHandler('im_user', im_user.im_user),
    CommandHandler('get_gid', get_gid.get_gid),
    CommandHandler('get_loc', get_loc.get_loc),
    CommandHandler('get_ctc', get_ctc.get_ctc),
    CommandHandler('get_doc', get_doc.get_doc),
    CommandHandler('db_len', db_len.db_len),
    CommandHandler('get_id', get_id.get_id)
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