import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Configure logging
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger()

# Your bot's token and channel ID
TOKEN = '7962771746:AAGmfNGa3iI46okfZ5kzyah8JL95baV8KT0'
CHANNEL_ID = '-1002265081796'

# Queue for storing posts (photo ID and caption)
posts_queue = []


# Function to send the next post from the queue
async def send_post(context: CallbackContext):
    global posts_queue

    if posts_queue:
        photo_id, caption = posts_queue.pop(0)  # Get the next post
        try:
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=photo_id, caption=caption)
            logger.info(f"Successfully sent post: {caption}")
        except Exception as e:
            logger.error(f"Failed to send post: {e}")
    else:
        logger.info("No posts in the queue.")


# Handle /start command
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Welcome! Send me images with captions, and I'll queue them for posting every 30 minutes.")


# Handle incoming image posts
async def queue_post(update: Update, context: CallbackContext):
    global posts_queue
    if update.message.photo and update.message.caption:
        photo_id = update.message.photo[-1].file_id
        caption = update.message.caption

        # Add post to queue
        posts_queue.append((photo_id, caption))
        await update.message.reply_text(f"Post queued. {len(posts_queue)} posts in the queue.")
        logger.info(f"Post added to queue. Queue size: {len(posts_queue)}.")
    else:
        await update.message.reply_text("Please send a photo with a caption.")


# Main function to run the bot
def main():
    # Create bot application with JobQueue support
    application = Application.builder().token(TOKEN).build()

    # Ensure JobQueue is set up
    job_queue = application.job_queue

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.PHOTO, queue_post))

    # Schedule jobs to send posts every 30 minutes
    job_queue.run_repeating(send_post, interval=30 * 60, first=0)  # 30 minutes in seconds

    # Start bot polling
    application.run_polling()


if __name__ == "__main__":
    main()
