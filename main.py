import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from dotenv import load_dotenv

# .env fayldan tokenni olish
load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"


# === FAYL BILAN ISHLASH FUNKSIYALARI ===
def load_data():
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except:
        return {"admin_id": None, "invites": {}}


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


data = load_data()


# === START KOMANDASI ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.reply(
        "👋 Salom! Men guruh uchun hisoblovchi botman.\n\n"
        "👤 Admin /setadmin buyrug‘i bilan o‘zini o‘rnatadi.\n"
        "📊 Bot yangi a’zolarni hisoblaydi va statistika yuritadi."
    )


# === ADMIN O‘RNATISH ===
@dp.message(Command("setadmin"))
async def set_admin(message: types.Message):
    if message.from_user:
        data["admin_id"] = message.from_user.id
        save_data(data)
        await message.reply("✅ Siz admin sifatida o‘rnatildingiz!")


# === BOTNI ISHGA TUSHURISH ===
async def main():
    print("🤖 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
