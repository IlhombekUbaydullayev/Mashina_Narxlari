import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from scraper import fetch_car_prices
import os
from datetime import datetime

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

async def send_car_prices():
    data = await fetch_car_prices()
    if data:
        today = datetime.now().strftime("%d-%B, %Y")
        msg = f"🚗 <b>Mashina narxlari – Spot.uz ({today}):</b>\n\n"
        for line in data["prices"]:
            msg += f"• {line}\n"
        msg += f"\n🔗 <a href='{data['url']}'>To‘liq maqola</a>"

        await bot.send_message(chat_id=CHANNEL_ID, text=msg, parse_mode="HTML")

async def scheduler():
    while True:
        now = datetime.now()
        if now.hour == 9 and now.minute == 0:
            await send_car_prices()
            await asyncio.sleep(60)  # bir daqiqa kutish, takrorlanmasin
        await asyncio.sleep(30)

async def main():
    asyncio.create_task(scheduler())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
