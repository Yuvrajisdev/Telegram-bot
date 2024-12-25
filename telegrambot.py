from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Your Bot API Token
BOT_TOKEN = "7962771746:AAGmfNGa3iI46okfZ5kzyah8JL95baV8KT0"
CHANNEL_ID = "-1002265081796"  # Replace with your channel ID

# Queue for storing messages
post_queue = []

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Hello! Send me any post (image, text, video), and I will forward it to your channel every 30 minutes.")

# Function to handle received posts
async def handle_post(update: Update, context: CallbackContext) -> None:
    post_queue.append(update.message)
    await update.message.reply_text(f"Post added. {len(post_queue)} posts are in queue.")

# Function to forward posts to the channel
async def send_post(context: CallbackContext) -> None:
    if post_queue:
        post = post_queue.pop(0)
        if post.photo:
            await context.bot.send_photo(chat_id=CHANNEL_ID, photo=post.photo[-1].file_id, caption=post.caption)
        elif post.video:
            await context.bot.send_video(chat_id=CHANNEL_ID, video=post.video.file_id, caption=post.caption)
        elif post.text:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=post.text)

# Main function
def main() -> None:
    # Create the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_post))

    # Job queue for forwarding posts every 30 minutes
    job_queue = application.job_queue
    job_queue.run_repeating(send_post, interval=30 * 60, first=0)  # Every 30 minutes

    # Run the bot
    application.run_polling()

if __name__ == "__main__":
    main()
