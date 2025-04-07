import requests
import os
from dotenv import load_dotenv

load_dotenv()

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
BOARD_ID = os.getenv("TRELLO_BOARD_ID")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # URL da Vercel, ex: https://seuprojeto.vercel.app/api/trello-webhook

def registrar_webhook():
    url = "https://api.trello.com/1/webhooks"
    payload = {
        "key": TRELLO_KEY,
        "token": TRELLO_TOKEN,
        "description": "Webhook Power-Up Auto ID",
        "callbackURL": WEBHOOK_URL,
        "idModel": BOARD_ID
    }

    response = requests.post(url, data=payload)

    if response.status_code == 200:
        print("✅ Webhook registrado com sucesso!")
        print("🔗 ID do Webhook:", response.json().get("id"))
    else:
        print("❌ Erro:", response.status_code)
        print(response.text)

if __name__ == '__main__':
    registrar_webhook()
