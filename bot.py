import logging
import random
import os
import asyncio
import httpx
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@your_channel"  # غيّرها لاسم قناتك
QARI_NAME = "هيثم الدخين"

SURAH_LIST = [
    "001.mp3", "002.mp3", "003.mp3", "004.mp3", "005.mp3",  # أكمل حسب ما تحتاج
]

SURAH_NAMES = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة",
]

# إرسال سورة كل 5 دقائق
async def send_surah_loop(app):
    while True:
        index = random.randint(0, len(SURAH_LIST) - 1)
        audio_file = SURAH_LIST[index]
        surah_name = SURAH_NAMES[index]

        url = f"https://server8.mp3quran.net/haitham/{audio_file}"
        caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"

        try:
            await app.bot.send_audio(chat_id=CHANNEL_ID, audio=url, caption=caption)
        except Exception as e:
            print(f"خطأ في الإرسال: {e}")

        await asyncio.sleep(300)  # كل 5 دقائق

# أوامر التلقرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت قران بصوت هيثم الدخين.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل الآن.")

async def random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = random.randint(0, len(SURAH_LIST) - 1)
    audio_file = SURAH_LIST[index]
    surah_name = SURAH_NAMES[index]
    url = f"https://server8.mp3quran.net/haitham/{audio_file}"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
    await update.message.reply_audio(audio=url, caption=caption)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("random", random_surah))

    # إرسال تلقائي كل 5 دقائق
    asyncio.create_task(send_surah_loop(app))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
