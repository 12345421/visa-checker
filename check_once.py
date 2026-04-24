"""
بوت مراقبة فيزا هولندا - نسخة GitHub Actions (تشتغل مرة واحدة)
"""

import requests
import os
from datetime import datetime

TELEGRAM_BOT_TOKEN = "8739687414:AAEMUxWbb4Df5HjsTCUqW5An0P5-nULz_1c"
TELEGRAM_CHAT_ID   = "8377577325"

VFS_URL = "https://visa.vfsglobal.com/mar/en/nld/book-an-appointment"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

UNAVAILABLE_KEYWORDS = [
    "no appointment",
    "no slots",
    "no available",
    "currently unavailable",
    "not available",
    "appointments are not available",
]

AVAILABLE_KEYWORDS = [
    "book appointment",
    "book an appointment",
    "select appointment",
    "available",
    "book now",
]

def send_telegram(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
    try:
        r = requests.post(url, data=data, timeout=10)
        print(f"Telegram: {r.status_code}")
    except Exception as e:
        print(f"Telegram error: {e}")

def check_appointments():
    try:
        session = requests.Session()
        session.get("https://visa.vfsglobal.com/mar/en/nld", headers=HEADERS, timeout=15)
        import time; time.sleep(2)
        r = session.get(VFS_URL, headers=HEADERS, timeout=15)
        page_text = r.text.lower()

        for kw in UNAVAILABLE_KEYWORDS:
            if kw in page_text:
                return "unavailable"
        for kw in AVAILABLE_KEYWORDS:
            if kw in page_text:
                return "available"
        return "unknown"
    except Exception as e:
        print(f"Error: {e}")
        return "error"

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] Checking VFS Global...")

    status = check_appointments()
    print(f"Status: {status}")

    if status == "available":
        send_telegram(
            "🚨 <b>توفرت مواعيد فيزا هولندا!</b>\n\n"
            "📍 VFS Global - الرباط\n"
            "🇳🇱 Netherlands Schengen Visa\n\n"
            f"🔗 <a href='{VFS_URL}'>حجز الموعد هنا</a>\n\n"
            f"⏰ {now}\n\n"
            "⚡ <b>سارع بالحجز قبل ما تنتهي!</b>"
        )
    elif status == "unavailable":
        print("No appointments available.")
    elif status == "unknown":
        print("Could not determine status.")
    elif status == "error":
        print("Connection error.")

if __name__ == "__main__":
    main()
