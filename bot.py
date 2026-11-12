import os
import threading
import telebot
import google.generativeai as genai
from flask import Flask

web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Dark Horror Bot is Live!"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_web, daemon=True).start()

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Welcome to Dark Horror Bot! Koi bhi horror topic bhejo, jaise Bhootiya Haveli.")

@bot.message_handler(func=lambda m: True)
def horror_reply(message):
    try:
        user_text = message.text
        bot.send_chat_action(message.chat.id, 'typing')
        prompt = "Ek darr wali horror kahani likho Hinglish me, 250 words me. Topic: " + user_text
        response = model.generate_content(prompt)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Bhoot busy hai, thodi der baad try karo!")
        print(e)

print("Bot Started...")
bot.infinity_polling()
