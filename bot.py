import re
import time
import asyncio
from collections import defaultdict

from aiogram import Bot, Dispatcher
from aiogram.types import Message

TOKEN = "8721489660:AAGbH2wioVZgmPu-qpxVubvvRhjJXRqXrJY"
CHANNEL_ID = -1003083716539

bot = Bot(token=TOKEN)
dp = Dispatcher()

# хранение сообщений
ip_messages = defaultdict(list)

TIME_WINDOW = 60
MAX_REQUESTS = 5

def extract_ip(text):
    match = re.search(r"(\d{1,3}(?:\.\d{1,3}){3})", text)
    return match.group(1) if match else None

async def process_ip(ip):
    await asyncio.sleep(TIME_WINDOW)

    messages = ip_messages[ip]

    if len(messages) < MAX_REQUESTS:
        print(f"✅ ЛИД: {ip}")

        for msg in messages:
            await bot.send_message(
                chat_id=CHANNEL_ID,
                text=f"✅ ЛИД\n\n{msg}"
            )
    else:
        print(f"❌ СПАМ: {ip}")

    # очищаем
    ip_messages[ip] = []

@dp.message()
async def handle_message(message: Message):
    text = message.text or ""

    ip = extract_ip(text)

    if not ip:
        return

    ip_messages[ip].append(text)

    # если это первое сообщение — запускаем таймер
    if len(ip_messages[ip]) == 1:
        asyncio.create_task(process_ip(ip))

async def main():
    print("Bot started...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
