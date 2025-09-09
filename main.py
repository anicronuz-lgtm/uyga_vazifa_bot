import telebot
from telebot import types
import os
import json

TOKEN = os.getenv("TOKEN")  # Token Railway'dagi Environment'dan olinadi
bot = telebot.TeleBot(TOKEN)

FILENAME = "tasks.json"

# Faylni o‘qish
def load_tasks():
    try:
        with open(FILENAME, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

# Faylga yozish
def save_tasks(tasks):
    with open(FILENAME, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

tasks = load_tasks()

# /start komandasi
@bot.message_handler(commands=['start'])
def start_message(message):
    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📘 Uy vazifani ko‘rish", callback_data="show_tasks"))
    bot.send_message(message.chat.id, f"👋 Salom, {username}!", reply_markup=markup)

# Tugmalarni boshqarish
@bot.callback_query_handler(func=lambda call: call.data == "show_tasks")
def select_day(call):
    markup = types.InlineKeyboardMarkup()
    days = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    for day in days:
        markup.add(types.InlineKeyboardButton(day, callback_data=f"day_{day}"))
    bot.edit_message_text("📅 Qaysi hafta kunini tanlaysiz?", call.message.chat.id, call.message.message_id, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("day_"))
def show_day_tasks(call):
    day = call.data.split("_")[1]
    data = load_tasks()
    if day not in data or not data[day]:
        text = f"📭 {day} kuni uchun vazifa yo‘q."
    else:
        text = f"📘 {day} kuni vazifalari:\n"
        for t in data[day]:
            text += f" - {t['task']} (👤 {t['author']})\n"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text)

print("✅ Bot ishga tushdi (Railway)")
bot.infinity_polling()

