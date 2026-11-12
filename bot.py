import os
import threading
import telebot
import google.generativeai as genai
from flask import Flask

# --- Render ke liye Port wala jugad ---
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Dark Horror Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()
# ----------------------------------------

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👻 Welcome to Dark Horror Bot!\n\nKoi bhi horror topic bhejo, jaise:\n- Bhootiya Haveli\n- Raat 3 baje ka call\n- Chudail ki kahani\n\nMain tumhare liye darr wali kahani likhunga!")

@bot.message_handler(func=lambda m: True)
def horror_reply(message):
    try:
        user_text = message.text
        bot.send_chat_action(message.chat.id, 'typing')
        
        prompt = f"Ek bahut hi darr wali, dark horror kahani likho Hindi/Hinglish me. Topic: {user_text}. Kahani 250 words me
