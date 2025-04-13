import os
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Impostazioni di Telegram
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
updater = Updater(TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Impostazioni di OpenAI
openai.api_key = os.environ.get("OPENAI_KEY")

# Funzione di risposta del bot
def start(update, context):
    update.message.reply_text("Ciao! Sono NutriMente, il tuo coach virtuale di benessere. Inviami un messaggio e ti risponderò!")

def chat(update, context):
    user_message = update.message.text
    response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=user_message,
        max_tokens=150
    )
    update.message.reply_text(response.choices[0].text.strip())

# Gestione dei comandi
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
message_handler = MessageHandler(Filters.text & ~Filters.command, chat)
dispatcher.add_handler(message_handler)

# Avvia il bot
updater.start_polling()
updater.idle()
