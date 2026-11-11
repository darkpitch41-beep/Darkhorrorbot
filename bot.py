import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
import threading

TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
@app.route('/')
def home():
    return "Automation Bot Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 AI Automation Bot ON hai!\n\n"
        "Video banane ke liye likho:\n"
        "/video Kali Haveli\n\n"
        "Ya apna topic likho:\n"
        "/video Aakhri Train"
    )

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Pehle topic likho bhai!\nJaise: /video Kali Haveli")
        return

    topic = " ".join(context.args)
    await update.message.reply_text(f"⏳ {topic} pe tera video ban raha hai... 30 sec ruk...")

    # AUTO SCRIPT - 6 Scene
    script = f"""🎬 TERA VIDEO READY HAI - TOPIC: {topic}

--- SCENE 1: SHURUAT ---
🎙️ VOICEOVER: "Raat ke 12 baje, {topic} ki kahani shuru hoti hai. Gaon wale kehte hai, waha jo gaya, wapas nahi aaya."
🖼️ IMAGE PROMPT: Dark horror night, foggy village, old {topic}, cinematic, scary atmosphere, 9:16
🔊 SOUND: Slow heartbeat + wind

--- SCENE 2: ENTRY ---
🎙️ VOICEOVER: "Rohan ne himmat ki, aur andar kadam rakha. Darwaza apne aap band ho gaya."
🖼️ IMAGE PROMPT: Young boy entering dark old house, door closing, horror lighting, 9:16
🔊 SOUND: Door creak + thunder

--- SCENE 3: AWAAZ ---
🎙️ VOICEOVER: "Achanak upar se kisi ke chalne ki awaaz aayi. Rohan ka dil zor se dhadakne laga."
🖼️ IMAGE PROMPT: Dark staircase, shadow on wall, horror, scary, 9:16
🔊 SOUND: Footsteps

--- SCENE 4: CHEHRA ---
🎙️ VOICEOVER: "Jab usne peeche mud ke dekha, to waha koi khada tha... jiska chehra nahi tha."
🖼️ IMAGE PROMPT: Faceless ghost standing behind boy, dark horror, scary face, 9:16
🔊 SOUND: Loud scream + horror sting

--- SCENE 5: BHAAGNA ---
🎙️ VOICEOVER: "Rohan ne bhaagna shuru kiya, par har darwaza band tha. Koi rasta nahi tha."
🖼️ IMAGE PROMPT: Boy running in dark corridor, horror, motion blur, scary, 9:16
🔊 SOUND: Fast running + breathing

--- SCENE 6: END /
