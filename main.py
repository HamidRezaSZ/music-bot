import logging
import os

from dotenv import load_dotenv

from services import *
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

load_dotenv(verbose=True)

BOT_TOKEN = os.getenv('BOT_TOKEN')


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_first_name = user.first_name

    message_id = update.effective_message.message_id
    text = f'Hi {user_first_name}'
    text2 = 'Whenever you want, you can type the name of the song to search'

    await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=message_id, text=text)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text2)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "Sorry, I didn't understand that command."
    message_id = update.effective_message.message_id

    await context.bot.send_message(chat_id=update.effective_chat.id, reply_to_message_id=message_id, text=text)


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name_of_song = update.message.text.lower()

    list_of_songs = search_on_all_services(name_of_song)

    reply_markup = InlineKeyboardMarkup(list_of_songs)

    await update.message.reply_text("List of songs:", reply_markup=reply_markup)


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    search_handler = MessageHandler(filters.TEXT, search)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(search_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
