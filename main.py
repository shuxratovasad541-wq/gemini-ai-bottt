import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import google.generativeai as genai
from flask import Flask
from threading import Thread

# --- SOZLAMALAR ---
TELEGRAM_TOKEN = "8417149761:AAFOME0yo_lCS81XSIZpyBMrwX6CzDk8iEg"
GEMINI_API_KEY = "AIzaSyAYZO8z7GWhySKuaIy7HQP98uOUkKjiCLo"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

app = Flask('')
@app.route('/')
def home(): return "Bot 24/7 ishlayapti!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Render serverida 24/7 ishlovchi AI botman! Savolingizni bering.")

@dp.message()
async def ai_handler(message: types.Message):
    await bot.send_chat_action(chat_id=message.chat.id, action="typing")
    try:
        response = model.generate_content(message.text)
        await message.answer(response.text, parse_mode="Markdown")
    except Exception as e:
        await message.answer("AI hozircha band. Birozdan so'ng urinib ko'ring.")

async def main():
    Thread(target=run_flask).start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
