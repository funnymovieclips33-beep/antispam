import re
import asyncio
from collections import defaultdict

from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = "8721489660:AAGbH2wioVZgmPu-qpxVubvvRhjJXRqXrJY"

# 👉 канал куда отправлять ЧИСТЫЕ лиды
TARGET_CHANNEL_ID = -1003083716539

bot = Bot(token=TOKEN)
dp = Dispatcher()

ip_messages = defaultdict(list)

TIME_WINDOW = 60
MAX_REQUESTS = 5

# 🔍 поиск IP
def extract_ip(text):
    match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", text)
    return match.group(1) if match else None

# ⏳ обработка пачки сообщений
async def process_ip(ip):
    print(f"⏳ Ждём {TIME_WINDOW} сек для IP {ip}")
    await asyncio.sleep(TIME_WINDOW)

    messages = ip_messages[ip]
    print(f"📊 Всего сообщений от {ip}: {len(messages)}")

    if len(messages) < MAX_REQUESTS:
        print(f"✅ ЛИД: {ip}")

        await bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"✅ ЛИД (IP: {ip})\n\n{messages[0]}"
        )
    else:
        print(f"❌ СПАМ: {ip}")

        await bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"⚠️ ПОДОЗРИТЕЛЬНЫЙ ЛИД (IP: {ip})\n\n{messages[0]}"
        )

    ip_messages[ip] = []

# 🔥 ОБРАБОТКА СООБЩЕНИЙ ИЗ КАНАЛА
@dp.channel_post()
async def handle_channel_post(message: Message):

    text = message.text or message.caption or ""

    print("📩 Новое сообщение из канала:", text)

    if not text.strip():
        return

    ip = extract_ip(text)
    print("🌐 IP:", ip)

    # без IP → сразу лид
    if not ip:
        await bot.send_message(
            chat_id=TARGET_CHANNEL_ID,
            text=f"✅ ЛИД (без IP)\n\n{text}"
        )
        return

    ip_messages[ip].append(text)

    if len(ip_messages[ip]) == 1:
        asyncio.create_task(process_ip(ip))
