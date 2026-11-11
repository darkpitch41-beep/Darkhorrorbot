import os
import random
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("TELEGRAM_TOKEN", "")
PORT = int(os.environ.get("PORT", 10000))

app = Flask(__name__)

@app.route("/")
def home():
    return "Dark Horror Bot is Live"

STORIES = [
    "Ek gaon me ek purani haveli thi. Raat 12 baje waha se kisi ke rone ki awaaz aati thi.",
    "Monday ki raat ek ladka akela jungle wale raste se ja raha tha. Piche se kisi ne uska naam liya.",
    "Ek purani diary mili, usme likha tha - Agar ye padh rahe ho, to piche mat dekhna.",
    "Ek school 20 saal se band tha. Ek raat uski khidki me light jalti dikhi."
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "Welcome to Dark Horror Bot. Main hoon Hindi Horror Storyteller. Story ke liye /story likh ke bhej de."
    await update.message.reply_text(msg)

async def story(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args) if context.args else "Purani Haveli"
    one = random.choice(STORIES)
    final = "TOPIC: " + topic + "\n\n" + one + "\n\nAage ki kahani ke liye /story dobara bhej."
    await update.message.reply_text(final)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Dar lag raha hai? /story likh, ek kahani sunata hu.")

def run_bot():
    if not TOKEN:
        print("TELEGRAM_TOKEN missing")
        return
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("story", story))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot Started")
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host="0.0.0.0", port=PORT)
