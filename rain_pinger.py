import re
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# CONFIG
WEBHOOK_URL    = "https://discord.com/api/webhooks/..."  # ← твій вебхук
ROLE_ID        = "123456789012345678"                     # ← твій role ID
RAIN_URL       = "https://rollbet.gg"
TRIGGER_MINUTE = 34
TRIGGERED      = set()
LAST_HOUR      = -1

def fetch_rain_amount():
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(RAIN_URL, headers=headers, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")
        btn = soup.find("button", string=lambda s: s and "Tip Rain" in s)
        if btn:
            match = re.search(r"\$[\d,]+\.\d{2}", btn.text)
            return match.group(0) if match else "N/A"
        return "N/A"
    except Exception as e:
        print(f"❌ Error fetching rain amount: {e}")
        return "N/A"

def send_discord_embed(rain_amount, start_time):
    embed = {
        "author": {
            "name": "Rain Notifier",
            "icon_url": "https://twemoji.maxcdn.com/v/latest/72x72/1f327.png"
        },
        "title": "🌧️ Rain Started! 💦",
        "description": f"Rain balance: **{rain_amount}**\n🔗 [Join the Rain!]({RAIN_URL})",
        "color": 0x1ABC9C,
        "thumbnail": {"url": "https://rollbet.gg/chip.png"},
        "fields": [
            {"name": "Start Time", "value": start_time, "inline": True},
            {"name": "Join Link", "value": RAIN_URL, "inline": True}
        ],
        "footer": {"text": "Triggered by Rain Notifier"},
        "timestamp": datetime.utcnow().isoformat()
    }

    payload = {
        "content": f"<@&{ROLE_ID}>",
        "allowed_mentions": {"parse": ["roles"]},
        "embeds": [embed]
    }
    resp = requests.post(WEBHOOK_URL, json=payload)
    if 200 <= resp.status_code < 300:
        print(f"✅ Sent embed at {datetime.now().strftime('%H:%M:%S')}")
    else:
        print(f"❌ Error {resp.status_code}: {resp.text}")

def check_and_trigger():
    global LAST_HOUR
    now = datetime.now()
    minute = now.minute
    second = now.second

    if now.hour != LAST_HOUR:
        TRIGGERED.clear()
        LAST_HOUR = now.hour

    if minute == TRIGGER_MINUTE and minute not in TRIGGERED and second < 5:
        start_time = now.strftime("%H:%M:%S")
        rain_amount = fetch_rain_amount()
        send_discord_embed(rain_amount, start_time)
        TRIGGERED.add(minute)

if __name__ == "__main__":
    while True:
        check_and_trigger()
        time.sleep(1 - (time.time() % 1))
