import json
import pytz
from datetime import time
from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8940981359:AAF3MvNa5Qe15D6ZfhBxDDbSQT6m8TLm7-g"
MY_CHAT_ID = 318823278

# بارگذاری سوالات
with open('questions.json', 'r', encoding='utf-8') as f:
    QUESTIONS = json.load(f)

user_progress = {"current_index": 0}

async def send_quiz(context: ContextTypes.DEFAULT_TYPE):
    idx = user_progress["current_index"]
    if idx >= len(QUESTIONS):
        await context.bot.send_message(chat_id=MY_CHAT_ID, text="🎉 تبریک! تمام سوالات آزمون NPPE دوره شدند.")
        return

    q = QUESTIONS[idx]
    q_text = q['question']
    if len(q_text) > 280:
        q_text = q_text[:277] + "..."

    await context.bot.send_poll(
        chat_id=MY_CHAT_ID,
        question=f"📌 NPPE Ethics #{q['id']}/{len(QUESTIONS)}\n\n{q_text}",
        options=q['options'],
        type=Poll.QUIZ,
        correct_option_id=q['correct_option'],
        is_anonymous=False
    )
    user_progress["current_index"] += 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سلام ريان عزیز! 🌿\n\n"
        "ربات مطالعه آزمون اخلاق و حقوق مهندسی (NPPE) فعال شد.\n"
        "روزانه ۲ سوال سر ساعت‌های ۹ صبح و ۶ عصر برای شما ارسال می‌شود.\n\n"
        "برای دریافت فوری سوال بعدی، دستور /quiz را بزنید."
    )

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz_command))
    
    # تنظیم زمان‌بندی ارسال (ساعت ۹ صبح و ۶ عصر به وقت آلبرتا)
    tz = pytz.timezone("America/Edmonton")
    job_queue = app.job_queue
    job_queue.run_daily(send_quiz, time=time(hour=9, minute=0, tzinfo=tz))
    job_queue.run_daily(send_quiz, time=time(hour=18, minute=0, tzinfo=tz))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
