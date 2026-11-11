import os, re, textwrap, requests, asyncio, threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from PIL import Image, ImageDraw, ImageFont
from moviepy import ImageClip, AudioFileClip, concatenate_videoclips
import edge_tts

TOKEN = os.environ.get("BOT_TOKEN")
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Live Hai!"

IMAGES = [
    "https://images.unsplash.com/photo-1509557965875-b88c97052f0e?w=1080&q=80",
    "https://images.unsplash.com/photo-1519681393784-d120267933ba?w=1080&q=80",
    "https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=1080&q=80",
    "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1080&q=80",
    "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=1080&q=80"
]

# Khooni Monday jaisi gehari voice
async def make_voice(text):
    c = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="-12%", pitch="-12Hz")
    await c.save("voice.mp3")

def make_frame(img_path, text, out_path):
    img = Image.open(img_path).convert("RGB").resize((1080, 1920))
    overlay = Image.new("RGBA", (1080, 1920), (0,0,0,0))
    d2 = ImageDraw.Draw(overlay, "RGBA")
    d2.rectangle([0, 1200, 1080, 1920], fill=(0,0,0,150))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 56)
    except:
        font = ImageFont.load_default()
    lines = textwrap.wrap(text, width=26)
    y = 1320
    for line in lines:
        w = d.textbbox((0,0), line, font=font)[2]
        d.text(((1080-w)//2, y), line, font=font, fill="white", stroke_width=3, stroke_fill="black")
        y += 80
    img.save(out_path)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👻 Khooni Monday Style Bot Ready!\nApni story bhejo...")

async def make_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    story = update.message.text.strip()
    if len(story) < 20:
        await update.message.reply_text("Thodi lambi story bhejo!")
        return
    await update.message.reply_text("🎬 Khooni Monday style video bana raha hu... 2 min ruk ja...")
    try:
        await make_voice(story)
        audio = AudioFileClip("voice.mp3")
        total = audio.duration
        sentences = re.split(r'(?<=[।.!?])\s+', story)
        chunks = []
        cur = ""
        for s in sentences:
            if len(cur) + len(s) < 170:
                cur += " " + s
            else:
                chunks.append(cur.strip()); cur = s
        if cur: chunks.append(cur.strip())
        if not chunks: chunks = [story]
        per = total / len(chunks)
        clips = []
        for i, chunk in enumerate(chunks):
            url = IMAGES[i % len(IMAGES)]
            r = requests.get(url, timeout=15)
            open(f"img{i}.jpg","wb").write(r.content)
            make_frame(f"img{i}.jpg", chunk, f"frame{i}.jpg")
            clip = ImageClip(f"frame{i}.jpg").with_duration(per)
            clip = clip.resized(lambda t: 1 + 0.08 * t / per)
            clips.append(clip)
        final = concatenate_videoclips(clips, method="compose")
        final = final.with_audio(audio)
        final.write_videofile("final.mp4", fps=24, codec="libx264", audio_codec="aac", logger=None)
        await update.message.reply_video(video=open("final.mp4","rb"), caption="🔥 Khooni Monday Style Ready!")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

def run_bot():
    app2 = ApplicationBuilder().token(TOKEN).build()
    app2.add_handler(CommandHandler("start", start))
    app2.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, make_video))
    app2.run_polling()

threading.Thread(target=run_bot, daemon=True).start()
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
