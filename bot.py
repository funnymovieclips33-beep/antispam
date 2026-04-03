import re
import asyncio
from collections import defaultdict

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

TOKEN = "8721489660:AAGbH2wioVZgmPu-qpxVubvvRhjJXRqXrJY"
CHANNEL_ID = -1003083716539

bot = Bot(token=TOKEN)
dp = Dispatcher()

ip_messages = defaultdict(list)

TIME_WINDOW = 60
MAX_REQUESTS = 5

def extract_ip(text):
    match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", text)
    return match.group(1) if match else None

async def process_ip(ip):
    print(f"⏳ Ждём {TIME_WINDOW} сек для IP {ip}")
    await asyncio.sleep(TIME_WINDOW)

    messages = ip_messages[ip]
    print(f"📊 Всего сообщений от {ip}: {len(messages)}")

    if len(messages) < MAX_REQUESTS:
        print(f"✅ ЛИД: {ip}")

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"✅ ЛИД (IP: {ip})\n\n{messages[0]}"
        )
    else:
        print(f"❌ СПАМ: {ip}")

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"⚠️ ПОДОЗРИТЕЛЬНЫЙ ЛИД (IP: {ip})\n\n{messages[0]}"
        )

    ip_messages[ip] = []

# 🔥 ЛОВИМ ВСЁ (включая sender_chat)
@dp.message(F.text | F.caption)
async def handle_message(message: Message):

    # только группа
    if message.chat.type not in ["group", "supergroup"]:
        return

    text = message.text or message.caption or ""

    print("📩 Новое сообщение:", text)
    print("👤 from_user:", message.from_user)
    print("📢 sender_chat:", message.sender_chat)

    if not text.strip():
        print("❌ Пустое сообщение")
        return

    ip = extract_ip(text)
    print("🌐 IP:", ip)

    # без IP → сразу лид
    if not ip:
        print("⚠️ Нет IP → отправляем")

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"✅ ЛИД (без IP)\n\n{text}"
        )
        return

    ip_messages[ip].append(text)
    print(f"📦 Сохранили: {len(ip_messages[ip])}")

    if len(ip_messages[ip]) == 1:
        print(f"🚀 Таймер старт для {ip}")
        asyncio.create_task(process_ip(ip))

async def main():
    print("🤖 Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
