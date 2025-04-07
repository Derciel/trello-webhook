from flask import Flask, request
from vercel_wsgi import handle
import os
import requests

app = Flask(__name__)

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
CUSTOM_FIELD_ID = os.getenv("CUSTOM_FIELD_ID")

@app.route('/api/webhook', methods=['POST', 'GET'])
def trello_webhook():
    if request.method == 'GET':
        return 'Webhook ativo!'

    data = request.json
    action = data.get("action", {})
    if action.get("type") == "createCard":
        card_id = action.get("data", {}).get("card", {}).get("id")
        if card_id:
            powerup_id = "PU-" + os.urandom(4).hex().upper()
            requests.put(
                f"https://api.trello.com/1/card/{card_id}/customField/{CUSTOM_FIELD_ID}/item",
                params={"key": TRELLO_KEY, "token": TRELLO_TOKEN},
                json={"value": {"text": powerup_id}}
            )
    return '', 200

@app.route('/api/register_webhook', methods=['POST'])
def register_webhook():
    board_id = request.json.get("boardId")
    callback_url = os.getenv("WEBHOOK_URL")
    requests.post(
        'https://api.trello.com/1/webhooks/',
        params={
            'key': TRELLO_KEY,
            'token': TRELLO_TOKEN
        },
        json={
            'description': 'Webhook Trello para novo card',
            'callbackURL': callback_url,
            'idModel': board_id
        }
    )
    return '', 204

def handler(environ, start_response):
    return handle(app, environ, start_response)
