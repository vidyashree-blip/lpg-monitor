import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_alert(message):
    if "YOUR_BOT_TOKEN" in TELEGRAM_BOT_TOKEN:
        print(f"[ALERT - Telegram not set up yet]: {message}")
        return
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
        print("📱 Telegram alert sent!")
    except Exception as e:
        print(f"Notification error: {e}")