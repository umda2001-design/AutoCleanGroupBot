from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")

import os
import json
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

DATA_FILE = "data.json"

# --- Fayl bilan ishlash funksiyalari ---
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

# --- Start komandasi ---
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.reply("👋 Salom! Men guruh uchun hisoblovchi botman.\n"
                        "Admin /setadmin komandasidan foydalanib o‘zini o‘rnatsin.\n"
                        "Bot yangi a’zolarni hisoblaydi va statistikani yuritadi.")

# --- Adminni o‘rnatish ---
@dp.message_handler(commands=["setadmin"])
async def set_admin(message: types.Message):
    if not message.from_user:
        return

    if data["admin_id"] and message.from_user.id != data["admin_id"]:
        await message.reply("❌ Siz admin emassiz yoki admin allaqachon o‘rnatilgan.")
        return

    parts = message.text.split()
    if len(parts) < 2:
        await message.reply("Foydalanish: /setadmin <user_id>")
        return

    try:
        admin_id = int(parts[1])
    except:
        await message.reply("❌ ID faqat raqam bo‘lishi kerak.")
        return

    data["admin_id"] = admin_id
    save_data(data)
    await message.reply(f"✅ Admin o‘rnatildi: {admin_id}")

# --- Yangi foydalanuvchi qo‘shilganda ---
@dp.chat_member_handler()
async def on_user_join(event: types.ChatMemberUpdated):
    if event.new_chat_member and event.new_chat_member.status == "member":
        inviter = event.from_user
        new_user = event.new_chat_member.user

        if not inviter or inviter.is_bot:
            return

        user_id = str(inviter.id)
        if user_id not in data["invites"]:
            data["invites"][user_id] = {"name": inviter.full_name, "count": 0}

        data["invites"][user_id]["count"] += 1
        save_data(data)

        try:
            await bot.delete_message(event.chat.id, event.new_chat_member.user.id)
        except:
            pass

# --- Statistika komandasi ---
@dp.message_handler(commands=["stat"])
async def show_stats(message: types.Message):
    if not data["admin_id"]:
        await message.reply("⚠️ Admin hali o‘rnatilmagan.")
        return

    if message.from_user.id != data["admin_id"]:
        await message.reply("❌ Siz admin emassiz.")
        return

    if not data["invites"]:
        await message.reply("📊 Hozircha hech kim odam qo‘shmagan.")
        return

    text = "📊 Statistika:\n\n"
    for user_id, info in data["invites"].items():
        text += f"👤 {info['name']} — {info['count']} ta odam\n"
    await message.reply(text)

# --- Bot ishga tushganida ---
async def on_startup(_):
    print("🤖 Bot ishga tushdi...")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
