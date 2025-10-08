import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# Загружаем токен из .env или из переменных окружения Render
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"


# === Работа с файлом статистики ===
def load_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {"admin_id": None, "invites": {}}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


data = load_data()


# === Команда /start ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.reply(
        "👋 Привет! Я бот для подсчёта приглашений в группу.\n\n"  
        "👤 Администратор должен установить себя командой /setadmin.\n"
        "📊 После этого бот будет считать, кто сколько участников пригласил."
    )


# === Команда /setadmin ===
@dp.message(Command("setadmin"))
async def set_admin(message: types.Message):
    if message.from_user:
        data["admin_id"] = message.from_user.id
        save_data(data)
        await message.reply("✅ Вы успешно назначены администратором!")


# === Запуск бота ===
async def main():
    print("🤖 Бот запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
