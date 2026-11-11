import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
import threading
from gtts import gTTS
from PIL import Image, ImageDraw, ImageFont

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "Voice Bot Live!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Voice Automation Bot ON!\n\n"
        "Likho:\n/video Kali Haveli\n\n"
        "Bot Script + Voice + Thumbnail bana ke dega."
    )

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Topic likho: /video Kali Haveli")
        return

    topic = " ".join(context.args)
    await update.message.reply_text(f"⏳ {topic} pe kaam chal raha hai... Voice ban rahi hai...")

    # 1. SCRIPT
    voice_text = f"Raat ke 12 baje, {topic} ki kahani shuru hoti hai. Gaon wale kehte hai, waha jo gaya, wapas nahi aaya. Rohan ne himmat ki aur andar kadam rakha. Darwaza apne aap band ho gaya. Achanak upar se kisi ke chalne ki awaaz aayi. Jab usne peeche mud ke dekha, to waha koi khada tha, jiska chehra nahi tha. Rohan ne bhaagna shuru kiya, par har darwaza band tha. Subah gaon walo ko sirf uska phone mila."
    
    # 2. VOICE BANAO - gTTS
    try:
        tts = gTTS(text=voice_text, lang='hi', slow=False)
        tts.save("voice.mp3")
        await update.message.reply_audio(audio=open("voice.mp3", 'rb'), caption=f"🎙️ {topic} - Voiceover Ready!")
    except Exception as e:
        await update.message.reply_text(f"Voice me error aaya, par script de raha hu.")

    # 3. THUMBNAIL BANAO - Pillow
    try:
        img = Image.new('RGB', (1080, 1920), color=(0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((80, 800), topic.upper(), fill=(255, 0, 0))
        draw.text((80, 900), "HORROR STORY", fill=(255, 255, 255))
        img.save("thumb.jpg")
        await update.message.reply_photo(photo=open("thumb.jpg", 'rb'), caption="🖼️ Thumbnail Ready!")
    except Exception as e:
        pass

    # 4. SCRIPT BHEJO
    script = f"""🎬 {topic} - FULL PACKAGE

SCRIPT:
{voice_text}

IMAGE PROMPTS:
1. Dark horror night, foggy {topic}, scary, 9:16
2. Boy entering dark house, horror, 9:16
3. Dark staircase shadow, horror, 9:16
4. Faceless ghost behind boy, horror, 9:16
5. Boy running dark corridor, horror, 9:16
6. Broken phone on floor, horror ending, 9:16

Ab CapCut me: 6 Images + Ye Voice daal do = VIDEO READY ✅
"""
    await update.message.reply_text(script)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_flask, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("video", make_video))
    application.run_polling()
