import asyncio
import os
import json
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import ChatMemberUpdated
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

DATA_FILE = "data.json"


# --- Ma'lumotni faylda saqlash ---
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


# === START komandasi ===
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.reply(
        "👋 Привет! Я бот для подсчёта приглашений в группу.\n\n"
        "Чтобы назначить администратора, используйте /setadmin.\n"
        "Я автоматически удаляю уведомления о новых участниках и считаю, кто сколько людей пригласил."
    )


# === Adminni o‘rnatish ===
@dp.message(Command("setadmin"))
async def set_admin(message: types.Message):
    data["admin_id"] = message.from_user.id
    save_data(data)
    await message.reply("✅ Вы успешно назначены администратором!")


# === Foydalanuvchilarni kuzatish ===
@dp.chat_member(ChatMemberUpdated)
async def on_user_join(event: ChatMemberUpdated):
    # yangi foydalanuvchi qo‘shilganini aniqlash
    if event.new_chat_member.status == "member":
        inviter = event.from_user
        new_user = event.new_chat_member.user

        # xabarni o‘chirib tashlaymiz (joined)
        try:
            await bot.delete_message(event.chat.id, event.chat.id)
        except:
            pass

        if inviter and not inviter.is_bot:
            inviter_id = str(inviter.id)
            if inviter_id not in data["invites"]:
                data["invites"][inviter_id] = {"name": inviter.full_name, "count": 0}

            data["invites"][inviter_id]["count"] += 1
            save_data(data)


# === Statistika faqat admin uchun ===
@dp.message(Command("stat"))
async def show_stats(message: types.Message):
    if not data["admin_id"]:
        await message.reply("⚠️ Администратор ещё не назначен.")
        return

    if message.from_user.id != data["admin_id"]:
        await message.reply("🚫 У вас нет доступа к статистике.")
        return

    if not data["invites"]:
        await message.reply("📊 Пока никто никого не пригласил.")
        return

    text = "📊 Статистика приглашений:\n\n"
    for user_id, info in data["invites"].items():
        text += f"👤 {info['name']} — {info['count']} участников\n"

    await message.reply(text)


# === Botni ishga tushirish ===
async def main():
    print("🤖 Бот запущен и работает...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
