import logging
import random
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# إعدادات البوت
BOT_TOKEN   = "ضع_رمز_البوت_هنا"
CHANNEL_ID  = "@dzmmm"  # تأكّد أن البوت مشرف بالقناة
QARI_PATH   = "haytham"  # مسار القارئ في mp3quran.net
QARI_NAME   = "هيثم الدخين"

# قائمة السور
SURAH_LIST = [
    "الفاتحة", "البقرة", "آل عمران", "النساء", "المائدة", "الأنعام", "الأعراف", "الأنفال",
    "التوبة", "يونس", "هود", "يوسف", "الرعد", "إبراهيم", "الحجر", "النحل", "الإسراء", "الكهف",
    "مريم", "طه", "الأنبياء", "الحج", "المؤمنون", "النور", "الفرقان", "الشعراء", "النمل",
    "القصص", "العنكبوت", "الروم", "لقمان", "السجدة", "الأحزاب", "سبأ", "فاطر", "يس", "الصافات",
    "ص", "الزمر", "غافر", "فصلت", "الشورى", "الزخرف", "الدخان", "الجاثية", "الأحقاف", "محمد",
    "الفتح", "الحجرات", "ق", "الذاريات", "الطور", "النجم", "القمر", "الرحمن", "الواقعة", "الحديد",
    "المجادلة", "الحشر", "الممتحنة", "الصف", "الجمعة", "المنافقون", "التغابن", "الطلاق", "التحريم",
    "الملك", "القلم", "الحاقة", "المعارج", "نوح", "الجن", "المزمل", "المدثر", "القيامة", "الإنسان",
    "المرسلات", "النبأ", "النازعات", "عبس", "التكوير", "الانفطار", "المطففين", "الانشقاق",
    "البروج", "الطارق", "الأعلى", "الغاشية", "الفجر", "البلد", "الشمس", "الليل", "الضحى",
    "الشرح", "التين", "العلق", "القدر", "البينة", "الزلزلة", "العاديات", "القارعة", "التكاثر",
    "العصر", "الهمزة", "الفيل", "قريش", "الماعون", "الكوثر", "الكافرون", "النصر", "المسد",
    "الإخلاص", "الفلق", "الناس"
]

# متغيرات الحالة
is_running = True
sent_count = 0

# إعداد اللوق
logging.basicConfig(level=logging.INFO)

# إرسال سورة عشوائية كل 5 دقائق
async def send_random_surah(context: ContextTypes.DEFAULT_TYPE):
    global sent_count, is_running
    if not is_running:
        return

    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num  = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"

    try:
        await context.bot.send_audio(
            chat_id=CHANNEL_ID,
            audio=url,
            caption=caption
        )
        sent_count += 1
    except Exception as e:
        logging.error(f"فشل الإرسال: {e}")

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 أهلاً! هذا بوت سور القرآن الكريم بصوت هيثم الدخين.")

async def now(update: Update, context: ContextTypes.DEFAULT_TYPE):
    index = random.randint(0, 113)
    surah_name = SURAH_LIST[index]
    surah_num = str(index + 1).zfill(3)
    url = f"https://server6.mp3quran.net/{QARI_PATH}/{surah_num}.mp3"
    caption = f"📖 {surah_name}\n🎙️ {QARI_NAME}"
    await update.message.reply_audio(audio=url, caption=caption)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    state = "✅ يعمل" if is_running else "⏸️ متوقف"
    await update.message.reply_text(f"حالة البوت: {state}")

# نقطة التشغيل
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # أوامر المستخدم
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("now", now))
    app.add_handler(CommandHandler("status", status))

    # جدولة إرسال السور
    app.job_queue.run_repeating(send_random_surah, interval=300, first=0)

    app.run_polling()

if __name__ == "__main__":
    main()
