import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import asyncio
import os
import httpx

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = "@اسم_قناتك"  # بدون روابط، فقط اسم القناة
QARI_NAME = "هيثم الدخين"

# قائمة بسور القرآن كاملة
SURAH_LIST = [
    "001.mp3", "002.mp3", "003.mp3",  # وهكذا...
]

SURAH_NAMES = [
    "الفاتحة", "البقرة", "آل عمران",  # وهكذا...
]

async def send_random_surah(app):
    while True:
        index = random.randint(0, len(SURAH_LIST) - 1)
        surah_file = SURAH_LIST[index]
        surah_name = SURAH_NAMES[index]

        url = f"https://server8.mp3quran.net/haitham/{surah_file}"
        caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            if response.status_code == 200:
                await app.bot.send_audio(chat_id=CHANNEL_ID, audio=url, caption=caption)
        
        await asyncio.sleep(300)  # كل 5 دقائق

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحبًا! أنا بوت قرآن هيثم الدخين. أرسل /random لإرسال سورة الآن.")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت يعمل الآن.")

async def random_surah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = random.randint(0, len(SURAH_LIST) - 1)
    surah_file = SURAH_LIST[index]
    surah_name = SURAH_NAMES[index]
    url = f"https://server8.mp3quran.net/haitham/{surah_file}"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
    await update.message.reply_audio(audio=url, caption=caption)

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("random", random_surah))

    # ابدأ المهمة الخلفية للإرسال كل 5 دقائق
    asyncio.create_task(send_random_surah(app))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
