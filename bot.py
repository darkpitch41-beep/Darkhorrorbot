import os, requests, threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask

TOKEN = os.environ.get("BOT_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live on Koyeb!"

def get_script(topic):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_KEY}"
    prompt = f"Tu Horror YouTube Script Writer hai. Topic: {topic}. Mujhe 15 minute ki Horror Story likh de Hindi me, 2000 words me. Hook, 3 Scenes, Climax. Last me 15 Image Prompts English me de, 9:16 horror style."
    data = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        r = requests.post(url, json=data, timeout=60)
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return "Gemini se script nahi aaya, API Key check kar. Error: " + str(e)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 Bot ON hai! Koyeb Free Forever!\n\nLikho: /video Kali Haveli")

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "Kali Haveli"
    await update.message.reply_text(f"⏳ {topic} ki 15 min wali script likh raha hu... 1 min ruk ja...")
    script = get_script(topic)
    # Telegram 4000 char limit isliye tukdo me bhejte hai
    for i in range(0, len(script), 4000):
        await update.message.reply_text(script[i:i+4000])

def run_flask():
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    app2 = Application.builder().token(TOKEN).build()
    app2.add_handler(CommandHandler("start", start))
    app2.add_handler(CommandHandler("video", make_video))
    app2.run_polling()
