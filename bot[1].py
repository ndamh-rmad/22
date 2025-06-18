import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    JobQueue,
)
import os

# إعدادات البوت
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@dzmmm")  # قناة النشر
QARI_NAME = "هيثم الدخين"
QARI_PATH = "haytham_dokhayn"

# قائمة السور
SURAH_LIST = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف",
    "الأنفال", "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر",
    "النحل", "الإسراء", "الكهف", "مريم", "طه", "الأنبياء", "الحج", "المؤمنون",
    "النور", "الفرقان", "الشعراء", "النمل", "القصص", "العنكبوت", "الروم", "لقمان",
    "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات", "ص", "الزمر", "غافر",
    "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد", "الفتح",
    "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة",
    "الحديد", "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون",
    "التغابن", "الطلاق", "التحريم", "الملك", "القلم", "الحاقة", "المعارج", "نوح",
    "الجن", "المزمل", "المدثر", "القيامة", "الإنسان", "المرسلات", "النبأ", "النازعات",
    "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق", "البروج", "الطارق", "الأعلى",
    "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى", "الشرح", "التين",
    "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر",
    "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر",
    "المسد", "الإخلاص", "الفلق", "الناس"
]

# حالة التشغيل
is_running = True
sent_count = 0

# اللوق
logging.basicConfig(level=logging.INFO)

# ترسل سورة كل 5 دقايق
async def send_random_surah(context: ContextTypes.DEFAULT_TYPE):
    global sent_count, is_running
    if not is_running:
        return

    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}
🎙️ {QARI_NAME}"

    try:
        await context.bot.send_audio(
            chat_id=CHANNEL_ID,
            audio=url,
            caption=caption
        )
        sent_count += 1
    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")

# أوامر التلقرام
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 مرحباً! بوت تلاوات هيثم الدخين يعمل 🎧")

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "✅ شغال" if is_running else "⏸️ متوقف"
    await update.message.reply_text(f"الحالة: {state}
📊 أُرسلت {sent_count} سورة.")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}
🎙️ {QARI_NAME}"

    await update.message.reply_audio(audio=url, caption=caption)

# تشغيل البوت
async def main():
    global app
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("now", now))

    job_queue = app.job_queue
    job_queue.run_repeating(send_random_surah, interval=300, first=10)

    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
