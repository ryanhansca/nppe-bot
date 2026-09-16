import pytz
from datetime import time
from telegram import Update, Poll
from telegram.ext import Application, CommandHandler, ContextTypes

BOT_TOKEN = "8940981359:AAF3MvNa5Qe15D6ZfhBxDDbSQT6m8TLm7-g"
MY_CHAT_ID = 318823278

# بانک نمونه سوالات NPPE Ethics (مستقیم داخل کد)
QUESTIONS = [
    {
        "id": 1,
        "question": "Countries like the United States do not self-regulate their engineering profession. In contrast, Canadian engineers are self-regulated. What is the meaning of a 'self-regulating' profession:",
        "options": [
            "A) A group of people who review each other's work.",
            "B) Each province/territory passed an Act to form an Association to regulate.",
            "C) An association ensures its members follow bylaws and pay dues.",
            "D) Interprovincial teams that police the decisions of members."
        ],
        "correct_option": 1
    },
    {
        "id": 2,
        "question": "At Roller Coaster Inc, a team designs a structure. The drawings cover several engineering disciplines. How many people should seal the drawing?",
        "options": [
            "A) One",
            "B) Up to five",
            "C) Everyone involved in the project",
            "D) One for approving professional and one for each discipline"
        ],
        "correct_option": 3
    },
    {
        "id": 3,
        "question": "Jane, P.Geo., developed technology that benefits clients but reduces firm revenue. She proceeds because it produces greatest benefit for greatest number. This applies:",
        "options": [
            "A) Aristotle's Virtue-Based Ethics",
            "B) Kant's Duty-Based Ethics",
            "C) Locke's Rights-Based Ethics",
            "D) Mill's Utilitarianism"
        ],
        "correct_option": 3
    },
    {
        "id": 4,
        "question": "Omar, P.Eng., didn't give a standard 20% discount to a desperate client to keep extra money as a secret. Omar actions violate:",
        "options": [
            "A) Fidelity to public needs",
            "B) The reasonable person test",
            "C) Secret commission",
            "D) The Code of Ethics"
        ],
        "correct_option": 3
    }
]

current_index = 0

async def send_quiz(context: ContextTypes.DEFAULT_TYPE):
    global current_index
    if current_index >= len(QUESTIONS):
        await context.bot.send_message(chat_id=MY_CHAT_ID, text="🎉 دوره سوالات به پایان رسید.")
        return

    q = QUESTIONS[current_index]
    await context.bot.send_poll(
        chat_id=MY_CHAT_ID,
        question=f"📌 NPPE Ethics Question #{q['id']}\n\n{q['question']}",
        options=q['options'],
        type=Poll.QUIZ,
        correct_option_id=q['correct_option'],
        is_anonymous=False
    )
    current_index += 1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام ريان عزیز! 🌿\nربات NPPE Ethics فعال شد.\nبرای دریافت سوال /quiz را بزنید.")

async def quiz_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_quiz(context)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("quiz", quiz_command))
    
    tz = pytz.timezone("America/Edmonton")
    job_queue = app.job_queue
    job_queue.run_daily(send_quiz, time=time(hour=9, minute=0, tzinfo=tz))
    job_queue.run_daily(send_quiz, time=time(hour=18, minute=0, tzinfo=tz))

    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
