import os
import telegram
from flask import Flask, request
from dotenv import load_dotenv

# Carica variabili da .env
load_dotenv()

# Imposta il bot di Telegram
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Crea l'app Flask
app = Flask(__name__)

# Funzione per gestire il webhook
@app.route('/<token>', methods=['POST'])
def webhook(token):
    if token == TELEGRAM_TOKEN:
        update = telegram.Update.de_json(request.get_json(), bot)
        chat_id = update.message.chat_id
        text = update.message.text
        
        # Rispondi al messaggio
        bot.sendMessage(chat_id=chat_id, text=f"Hai scritto: {text}")
        return 'OK'
    return 'Unauthorized', 403

# Pagina di test per verificare che il server stia funzionando
@app.route('/')
def home():
    return "Bot di nutrizione e benessere in esecuzione!"

if __name__ == '__main__':
    # Usa gunicorn per eseguire il server in produzione (su Render)
    app.run(debug=True)
