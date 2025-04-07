import os
import requests
from dotenv import load_dotenv

load_dotenv()

TRELLO_KEY = os.getenv("TRELLO_KEY")
TRELLO_TOKEN = os.getenv("TRELLO_TOKEN")
TRELLO_BOARD_ID = os.getenv("TRELLO_BOARD_ID")

url = f"https://api.trello.com/1/boards/{TRELLO_BOARD_ID}/customFields"

params = {
    "key": TRELLO_KEY,
    "token": TRELLO_TOKEN
}

response = requests.get(url, params=params)

if response.status_code == 200:
    campos = response.json()
    if not campos:
        print("❌ Nenhum campo personalizado encontrado no board.")
    else:
        print("✅ Campos personalizados encontrados:\n")
        for campo in campos:
            print(f"ID:   {campo['id']}")
            print(f"Nome: {campo['name']}")
            print(f"Tipo: {campo['type']}")
            print("-" * 40)
else:
    print("❌ Erro ao buscar campos personalizados.")
    print("Código de status:", response.status_code)
    print("Resposta:", response.text)
