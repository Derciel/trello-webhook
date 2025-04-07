# api/index.py

import os
import requests
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Carrega as variáveis do ambiente
TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
CUSTOM_FIELD_ID = os.getenv("CUSTOM_FIELD_ID")

def gerar_id_powerup():
    return "PU-" + os.urandom(4).hex().upper()

@app.route('/api/webhook', methods=['GET', 'POST'])
def trello_webhook():
    if request.method == 'GET':
        return 'Webhook ativo!'

    data = request.json
    action = data.get("action", {})
    
    if action.get("type") == "createCard":
        card = action.get("data", {}).get("card", {})
        card_id = card.get("id")

        if card_id:
            powerup_id = gerar_id_powerup()
            url = f"https://api.trello.com/1/card/{card_id}/customField/{CUSTOM_FIELD_ID}/item"
            params = {"key": TRELLO_KEY, "token": TRELLO_TOKEN}
            payload = {"value": {"text": powerup_id}}

            response = requests.put(url, params=params, json=payload)

            if response.status_code == 200:
                return jsonify({"status": "success", "powerup_id": powerup_id})
            else:
                return jsonify({"status": "error", "detail": response.text}), response.status_code

    return jsonify({"status": "ignored"}), 200

# Apenas para testes locais
if __name__ == '__main__':
    app.run(debug=True)
