import psutil
import requests

# =====================
# Config
# Sent CPU / RAM / Disc usage in Telegram chat for Local machine
# =====================
BOT_TOKEN = "8414000798:AAF0Oby2OyqwXrILqP0OuHHffZavPNhtWXo"
# https://api.telegram.org/bot8414000798:AAF0Oby2OyqwXrILqP0OuHHffZavPNhtWXo/getUpdates
CHAT_ID = "8208739271"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("[OK] Message was sent in Telegram")
    else:
        print(f"[ERR] Telegram error: {response.text}")

def report_system_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage("/").percent

    message = (
        "System Report:\n"
        f"CPU: {cpu_usage}%\n"
        f"RAM: {memory_usage}%\n"
        f"Disk: {disk_usage}%"
    )
    send_telegram_message(message)

if __name__ == "__main__":
    report_system_usage()
