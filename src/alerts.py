import os
import httpx
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

async def send_telegram_alert(message: str):
    """Asynchronous sending of a message to Telegram"""
    if not TOKEN or not CHAT_ID:
        print("⚠️ Error: Telegram Token or Chat ID not found in .env file.")
        return

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                print(f"❌ Telegram API Error: {response.text}")
        except Exception as e:
            print(f"❌ Network error while sending alert: {e}")