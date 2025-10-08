from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import asyncio
import os

TOKEN = "8480300061:AAEr8Cs08Wxzu2F2waEwvzDHLbl2OJPHDqE"  # BotFather bergan tokenni shu joyga yoz

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(content_types=['text', 'photo', 'video', 'document'])
async def auto_delete(message: types.Message):
    await asyncio.sleep(30)  # 30 soniya kutadi (xohlasa 10 yoki 60 qil)
    try:
        await message.delete()
    except:
        pass

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("🧹 AutoCleanGroupBot ishlayapti! Xabarlar avtomatik o‘chadi.")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    executor.start_polling(dp, skip_updates=True)
