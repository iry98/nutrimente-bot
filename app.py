from flask import Flask, request
import telegram
import openai
import os

# Inizializza Flask
app = Flask(__name__)

# Legge i token dalle variabili di ambiente
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# Configura il bot di Telegram
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Inizializza client OpenAI
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# Webhook per ricevere messaggi da Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    chat_id = update.message.chat.id
    user_message = update.message.text

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Sei un assistente esperto in nutrizione e benessere."},
                {"role": "user", "content": user_message}
            ]
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        reply = f"Errore OpenAI: {str(e)}"

    bot.send_message(chat_id=chat_id, text=reply)
    return 'ok'
