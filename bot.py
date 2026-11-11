import os
import random
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

app = Flask(__name__)
@app.route('/')
def home():
    return "Dark Horror Bot is Live!"

TOKEN = os.environ.get("BOT_TOKEN")

STORIES = [
    "🏚️ THE LAST CALL\n\nRaat ke 3 baje Aarav ko unknown number se call aaya. Usne uthaya to sirf saans ki awaaz aayi... Agli subah uska phone history me wo number tha hi nahi. Par gallery me ek photo thi - uski sote hue ki, jo usne kabhi nahi li thi.",
    "🪞 SHEESHA\n\nRiya ne naye ghar me ek purana sheesha lagaya. Har raat 2:47 AM pe sheeshe me uska reflection 2 second late move karta tha. Ek raat usne pucha - Tum kaun ho? Reflection ne bola - Main Riya hu, tum kaun ho?",
    "🚗 HIGHWAY 47\n\nTruck driver ne raat ko highway pe ek ladki ko lift di. Wo chup-chap baithi rahi. Jab uske ghar pahuche to wo gayab thi. Sirf seat gili thi. Ghar pe uski maa ne bola - Meri beti to 5 saal pehle isi highway pe marr gayi thi.",
    "📱 LAST SEEN\n\nRohan ka dost 2 saal pehle marr gaya. Par kal raat uska WhatsApp Online dikha. Rohan ne Kaun? likha. Reply aaya - Kabristan me network accha hai, tu kab aa raha hai?",
    "🏥 WARD NO. 13\n\nHospital ke Ward 13 me koi patient nahi rehta. Par har raat nurse ko waha se bell bajne ki awaaz aati hai. Ek nayi nurse gayi to dekha, bed pe koi baitha tha. Usne bola - Meri dawai... main 10 saal se yahi hu.",
]

FACTS = [
    "Raat 3 baje ko Devil's Hour kehte hai, is time sabse zyada paranormal activity hoti hai.",
    "Mirror ke saamne 10 min tak bina palak jhapkaye dekhoge to tumhara chehra badalne lagega.",
    "Agar tumhe lag raha hai ki koi tumhe dekh raha hai, to 70% chance hai ki tumhara dimaag sahi keh raha hai.",
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("👻 Horror Story", callback_data="story"),
         InlineKeyboardButton("💀 Scary Fact", callback_data="fact")],
        [InlineKeyboardButton("🎲 Dare", callback_data="dare")],
    ]
    await update.message.reply_text(
        "Welcome to DARK HORROR BOT 👻\n\nRaat ke 12 baje ke baad is bot ko mat kholna...\nNeeche se choose kar, agar himmat hai to:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    keyboard = [[InlineKeyboardButton("🔄 Agli Story", callback_data="story"),
                 InlineKeyboardButton("🏠 Menu", callback_data="menu")]]
    if data == "story":
        await q.edit_message_text(random.choice(STORIES), reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "fact":
        await q.edit_message_text(f"💀 SCARY FACT:\n\n{random.choice(FACTS)}", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "dare":
        dares = ["Aaj raat 3 baje sheeshe me dekh ke apna naam 3 baar bolo.", "Apne kamre ki light band karke 1 min akela baitho.", "Chhat pe jaake ek baar peeche mud ke dekho bina dare."]
        await q.edit_message_text(f"🎲 DARE:\n\n{random.choice(dares)}", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "menu":
        await start(update, context)

def main():
    app_bot = ApplicationBuilder().token(TOKEN).build()
    app_bot.add_handler(CommandHandler("start", start))
    app_bot.add_handler(CallbackQueryHandler(button_handler))
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000), daemon=True).start()
    app_bot.run_polling()

if __name__ == "__main__":
    main()
