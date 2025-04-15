import os
from flask import Flask, request, redirect
import telegram
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, MessageHandler, Filters
import stripe
from stripe_config import create_checkout_session, is_user_subscribed

app = Flask(__name__)

TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telegram.Bot(token=TOKEN)

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    dp = Dispatcher(bot, None, workers=0)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, handle_message))
    dp.process_update(update)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot di nutrizione attivo", 200

@app.route("/subscribe/<chat_id>", methods=["GET"])
def subscribe(chat_id):
    return redirect(create_checkout_session(chat_id), code=303)

def start(update: Update, context):
    chat_id = update.message.chat.id
    if is_user_subscribed(str(chat_id)):
        context.bot.send_message(chat_id=chat_id, text="Bentornato! Scrivi un argomento per ricevere consigli nutrizionali.")
    else:
        url = f"https://TUO_DOMINIO_RENDER/subscribe/{chat_id}"
        context.bot.send_message(chat_id=chat_id, text=f"Per accedere ai contenuti, abbonati qui:\n{url}")

def handle_message(update: Update, context):
    chat_id = update.message.chat.id
    if is_user_subscribed(str(chat_id)):
        context.bot.send_message(chat_id=chat_id, text="Ecco un consiglio nutrizionale: bevi almeno 2 litri d'acqua al giorno.")
    else:
        url = f"https://TUO_DOMINIO_RENDER/subscribe/{chat_id}"
        context.bot.send_message(chat_id=chat_id, text=f"Per continuare, abbonati qui:\n{url}")
