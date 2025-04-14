import os
import openai
from flask import Flask, request

app = Flask(__name__)

# Prende la chiave API da una variabile d'ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route('/', methods=['GET'])
def home():
    return "Bot attivo!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    message = data.get("message", {}).get("text", "")

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": message}
            ]
        )
        reply = response['choices'][0]['message']['content']
        return {"response": reply}, 200

    except Exception as e:
        return {"error": f"Errore OpenAI: {str(e)}"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
