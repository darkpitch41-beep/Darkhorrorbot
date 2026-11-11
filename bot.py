
import os
import re
import asyncio
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from google import genai
from elevenlabs import ElevenLabs
from pydub import AudioSegment

load_dotenv()

# API KEYS
BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

# AI CLIENTS
gemini = genai.Client(api_key=GEMINI_API_KEY)

eleven = ElevenLabs(
    api_key=ELEVENLABS_API_KEY
)

MODEL = "gemini-3.8-flash"

OUTPUT = Path("output")
OUTPUT.mkdir(exist_ok=True)


# 1. GENERATE FULL HINDI HORROR STORY
def generate_story(topic):

    prompt = f"""
You are a professional Hindi horror storyteller
writing original stories for a YouTube channel.

TOPIC: {topic}

Write a complete Hindi horror story.

STRICT REQUIREMENTS:

1. Target narration duration: 10 minutes.
2. Approximately 1200-1400 Hindi words.
3. Use natural conversational Hindi.
4. Write in Devanagari script.
5. One narrator only.
6. No dialogue labels or screenplay format.
7. Dark, suspenseful and mysterious atmosphere.
8. Strong opening hook in the first 20 seconds.
9. Gradually increase fear and tension.
10. Include vivid cinematic descriptions.
11. Add unexpected twists.
12. End with a terrifying climax.
13. Give a memorable final ending.
14. No unnecessary introductions.
15. Story must be original.

Write narration only.
Do not explain your writing process.
"""

    response = gemini.models.generate_content(
        model=MODEL,
        contents=prompt
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty story")

    return response.text.strip()


# 2. SPLIT STORY INTO TTS-SAFE CHUNKS
def split_text(text, max_chars=2200):

    paragraphs = [
        p.strip() for p in text.split("\n")
        if p.strip()
    ]

    chunks = []
    current = ""

    for paragraph in paragraphs:

        while len(paragraph) > max_chars:
            if current:
                chunks.append(current)
                current = ""

            cut = paragraph.rfind("।", 0, max_chars)

            if cut < max_chars // 2:
                cut = paragraph.rfind(" ", 0, max_chars)

            if cut < 1:
                cut = max_chars

            chunks.append(paragraph[:cut].strip())
            paragraph = paragraph[cut:].strip()

        if len(current) + len(paragraph) + 1 > max_chars:
            if current:
                chunks.append(current)
            current = paragraph
        else:
            current = (current + "\n" + paragraph).strip()

    if current:
        chunks.append(current)

    return chunks


# 3. GENERATE CINEMATIC HINDI VOICE
def generate_voice(story, topic):

    chunks = split_text(story)

    combined = AudioSegment.empty()

    for index, chunk in enumerate(chunks):

        print(f"Generating voice {index + 1}/{len(chunks)}")

        audio_stream = eleven.text_to_speech.convert(
            voice_id=VOICE_ID,
            text=chunk,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128"
        )

        audio_bytes = b"".join(audio_stream)

        temp_file = OUTPUT / f"part_{index}.mp3"

        temp_file.write_bytes(audio_bytes)

        segment = AudioSegment.from_mp3(str(temp_file))

        combined += segment

        # Small natural pause between paragraphs
        combined += AudioSegment.silent(duration=350)

        temp_file.unlink(missing_ok=True)

    safe_name = re.sub(
        r"[^a-zA-Z0-9_-]+", "_", topic
    )[:45]

    audio_file = OUTPUT / f"{safe_name}.mp3"

    combined.export(
        str(audio_file),
        format="mp3",
        bitrate="128k"
    )

    return audio_file


# 4. START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👻 WELCOME TO HINDI HORROR AI BOT\n\n"
        "Send /make followed by your horror topic.\n\n"
        "Example:\n"
        "/make The Haunted Hostel Room 309\n\n"
        "I will create a complete Hindi horror "
        "story and cinematic voiceover."
    )


# 5. MAKE STORY COMMAND
async def make_story(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if not context.args:
        await update.message.reply_text(
            "Please provide a topic.\n"
            "Example: /make Haunted Village"
        )
        return

    topic = " ".join(context.args)

    status = await update.message.reply_text(
        "👻 Your horror story is being created..."
    )

    try:
        # Generate story
        story = await asyncio.to_thread(
            generate_story, topic
        )

        safe_name = re.sub(
            r"[^a-zA-Z0-9_-]+", "_", topic
        )[:45]

        text_file = OUTPUT / f"{safe_name}.txt"
        text_file.write_text(story, encoding="utf-8")

        await status.edit_text(
            "📖 Story ready!\n"
            "🎙️ Generating cinematic Hindi voice..."
        )

        # Generate voice
        audio_file = await asyncio.to_thread(
            generate_voice, story, topic
        )

        await status.edit_text(
            "✅ Your horror story is complete!"
        )

        # Send full story
        with text_file.open("rb") as f:
            await update.message.reply_document(
                document=f,
                filename="Hindi_Horror_Story.txt",
                caption="📖 Your complete Hindi horror script"
            )

        # Send full narration
        with audio_file.open("rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=topic[:60],
                caption="🎧 Complete Hindi Horror Narration"
            )

        # Clean up
        text_file.unlink(missing_ok=True)
        audio_file.unlink(missing_ok=True)

    except Exception as error:
        print("ERROR:", error)

        await status.edit_text(
            "❌ Something went wrong.\n"
            "Please check your API keys, voice ID, "
            "internet connection and server logs."
        )


# 6. MAIN BOT
def main():

    required = [
        BOT_TOKEN,
        GEMINI_API_KEY,
        ELEVENLABS_API_KEY,
        VOICE_ID
    ]

    if not all(required):
        raise ValueError(
            "Missing API keys. Check your .env file."
        )

    app = ApplicationBuilder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CommandHandler("make", make_story)
    )

    print("HORROR BOT IS RUNNING...")

    app.run_polling()


if __name__ == "__main__":
    main()
