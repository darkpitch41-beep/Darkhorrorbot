import os
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip
from PIL import Image, ImageDraw
import requests, threading

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live Hai!"

def get_bg():
    url = "https://images.unsplash.com/photo-1509557965875-b88c97052f0e?w=1080"
    r = requests.get(url)
    open("bg.jpg","wb").write(r.content)
    return "bg.jpg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👻 Horror Video Bot Ready!\nBas apni script bhej do, main Voice + Background ke saath VIDEO bana dunga.")

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    script = update.message.text
    await update.message.reply_text("⏳ Video ban raha hai... 30 sec wait karo...")
    try:
        tts = gTTS(text=script, lang='hi', slow=False)
        tts.save("voice.mp3")
        bg_path = get_bg()
        img = Image.open(bg_path).convert("RGB")
        img = img.resize((720, 1280))
        draw = ImageDraw.Draw(img)
        draw.text((40, 1100), script[:100], fill="white")
        img.save("final_bg.jpg")
        audio = AudioFileClip("voice.mp3")
        clip = ImageClip("final_bg.jpg").with_duration(audio.duration)
        clip = clip.with_audio(audio)
        clip.write_videofile("final_video.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)
        await update.message.reply_video(video=open("final_video.mp4","rb"), caption="🔥 Tera Video Ready Hai!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_video))
    application.run_polling()

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=10000)).start()
    main()
