from telegram import Update
from telegram.ext import ContextTypes

from . import DB, control
from .consts import get_msg, ADMINS

async def get(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await control('REGLAS', update, context)