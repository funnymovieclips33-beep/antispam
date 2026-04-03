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

# 🔍 универсальный поиск IP
def extract_ip(text):
    match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", text)
    return match.group(1) if match else None

# 🧠 проверка на спам
def is_spam(ip):
    now = time.time()
    ip_logs[ip] = [t for t in ip_logs[ip] if now - t < TIME_WINDOW]

    if len(ip_logs[ip]) >= MAX_REQUESTS:
        return True

    ip_logs[ip].append(now)
    return False

# 🤖 обработка сообщений
@dp.message()
async def handle_message(message: Message):
    text = message.text or ""

    print("TEXT:", text)

    ip = extract_ip(text)
    print("IP:", ip)

    if not ip:
        print("❌ IP НЕ НАЙДЕН")
        return

    if is_spam(ip):
        print(f"❌ СПАМ: {ip}")
        return

    print(f"✅ ЛИД: {ip}")

    try:
        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=text
        )
        print("✅ ОТПРАВЛЕНО В КАНАЛ")
    except Exception as e:
        print("❌ ОШИБКА ОТПРАВКИ:", e)

# 🚀 запуск
async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
