import os, requests
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import google.generativeai as genai
import edge_tts
from PIL import Image, ImageDraw
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_KEY")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 DARKHORRORMAKER Ready hai Boss!\n\n30 Min ka Video chahiye to likho:\n/video Bhootiya Hostel")

async def video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args)
    if not topic:
        await update.message.reply_text("Topic to do! Jaise: /video Bhootiya School")
        return
    await update.message.reply_text(f"Ok Boss! '{topic}' pe 30 MIN ka Video ban raha hai... 🕯️\n25-30 min ruk jao, Video + Thumbnail + Title bhejta hun.")
    try:
        prompt = f"Tum Khooni Monday jaisa Hindi Horror Storyteller ho. Topic: {topic}. 5000
