import os
from flask import Flask, request
import openai
import telegram

# Imposta le chiavi
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_KEY = os.environ.get("OPENAI_KEY")

# Configura bot e OpenAI
bot = telegram.Bot(token=TELEGRAM_TOKEN)
openai.api_key = OPENAI_KEY

# Flask per il webhook
app = Flask(__name__)

# Messaggio di benvenuto
WELCOME_TEXT = "Ciao! Sono NutriMente, il tuo coach virtuale per nutrizione e benessere. Scrivimi pure!"

# Gestione richieste webhook
@app.route("/webhook", methods=["POST"])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    message = update.message.text

    if message.lower() in ["/start", "ciao", "buongiorno"]:
        bot.send_message(chat_id=chat_id, text=WELCOME_TEXT)
        return "OK"

    try:
        # Risposta con OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un esperto di nutrizione, benessere e stile di vita sano. Rispondi in modo amichevole e utile."},
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content'].strip()
        bot.send_message(chat_id=chat_id, text=reply)
    except Exception as e:
        bot.send_message(chat_id=chat_id, text="C'è stato un errore nel risponderti. Riprova più tardi.")
        print("Errore:", e)

    return "OK"
