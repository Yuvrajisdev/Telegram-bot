from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os

# Add your bot token here
BOT_TOKEN = "7962771746:AAGmfNGa3iI46okfZ5kzyah8JL95baV8KT0"
QUEUE = []  # Queue for storing posts

async def start(update, context):
    await update.message.reply_text("Bot started! Send me posts to forward.")

async def add_post(update, context):
    """Adds a post to the queue."""
    QUEUE.append(update.message)
    await update.message.reply_text(f"Post added. {len(QUEUE)} posts are in queue.")

async def send_post(context):
    """Sends posts from the queue to the specified channel."""
    if QUEUE:
        channel_id = "-1002265081796"  # Replace with your channel ID
        message = QUEUE.pop(0)  # Get the first post in the queue
        if message.photo:
            await context.bot.send_photo(
                chat_id=channel_id,
                photo=message.photo[-1].file_id,
                caption=message.caption,
            )
        elif message.text:
            await context.bot.send_message(chat_id=channel_id, text=message.text)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Create a job queue
    job_queue = application.job_queue

    # Run the job queue for repeating tasks
    job_queue.run_repeating(send_post, interval=30 * 60, first=0)  # Every 30 minutes

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL, add_post))

    application.run_polling()

if __name__ == "__main__":
    main()
