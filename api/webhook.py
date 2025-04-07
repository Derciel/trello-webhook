from flask import Flask, request
import requests
import os

app = Flask(__name__)

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
CUSTOM_FIELD_ID = os.getenv("CUSTOM_FIELD_ID")

def gerar_id_powerup():
    return "PU-" + os.urandom(4).hex().upper()

@app.route('/trello-webhook', methods=['HEAD', 'POST'])
def trello_webhook():
    if request.method == 'HEAD':
        return '', 200  # Validação do Trello

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

            requests.put(url, params=params, json=payload)

    return '', 200
