import re
import time
from collections import defaultdict
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = "8721489660:AAGbH2wioVZgmPu-qpxVubvvRhjJXRqXrJY"
CHANNEL_ID = -1003083716539  # твой канал

bot = Bot(token=TOKEN)
dp = Dispatcher()

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

@dp.message()
async def handle_message(message: Message):
    text = message.text or ""

    ip = extract_ip(text)

    if not ip:
        return

    if is_spam(ip):
        print(f"❌ СПАМ: {ip}")
        return  # игнорируем спам

    print(f"✅ ЛИД1: {ip}")

    # отправка в канал
    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=text
    )

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
