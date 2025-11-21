import os
import requests
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
channel_id = os.getenv("TELEGRAM_CHANNEL_ID")

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
data = {
    "chat_id": channel_id,
    "text": "Тестове повідомлення від бота"
}

response = requests.post(url, data=data)
result = response.json()

if result.get("ok"):
    print(f"Повідомлення надіслано успішно. Chat ID: {result['result']['chat']['id']}")
else:
    print(f"Помилка: {result.get('description', 'Невідома помилка')}")