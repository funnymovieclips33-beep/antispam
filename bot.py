import re
import time
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "8721489660:AAGbH2wioVZgmPu-qpxVubvvRhjJXRqXrJY"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

ip_logs = defaultdict(list)
TIME_WINDOW = 60
MAX_REQUESTS = 5

def extract_ip(text):
    match = re.search(r"IP адрес отправителя:\s*([0-9\.]+)", text)
    return match.group(1) if match else None

def is_spam(ip):
    now = time.time()
    ip_logs[ip] = [t for t in ip_logs[ip] if now - t < TIME_WINDOW]

    if len(ip_logs[ip]) >= MAX_REQUESTS:
        return True

    ip_logs[ip].append(now)
    return False

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_group(message: types.Message):
    text = message.text

    ip = extract_ip(text)

    if not ip:
        return

    if is_spam(ip):
        await message.react("❌")
    else:
        await message.react("✅")

if __name__ == "__main__":
    executor.start_polling(dp)
