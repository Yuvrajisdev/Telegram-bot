from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# Queue for storing posts
post_queue = []

# Channel ID (replace with your channel's chat_id)
CHANNEL_ID = "-1002265081796"

# Add posts to the queue
async def add_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.photo:
        post = {"photo": update.message.photo[-1].file_id, "caption": update.message.caption}
        post_queue.append(post)
        await update.message.reply_text(f"Post added. {len(post_queue)} posts are in the queue.")
    else:
        await update.message.reply_text("Please send a photo to add to the queue.")

# Function to forward posts to the channel
async def send_post(context: ContextTypes.DEFAULT_TYPE):
    if post_queue:
        post = post_queue.pop(0)  # Get the first post in the queue
        await context.bot.send_photo(
            chat_id=CHANNEL_ID,
            photo=post["photo"],
            caption=post["caption"]
        )

# Main function to start the bot
def main():
    # Create application
    application = Application.builder().token("YOUR_BOT_API_TOKEN").build()

    # Add handlers
    application.add_handler(MessageHandler(filters.PHOTO, add_post))

    # Add JobQueue
    job_queue = application.job_queue
    job_queue.run_repeating(send_post, interval=30 * 60, first=0)  # Run every 30 minutes

    # Run bot
    application.run_polling()

if __name__ == "__main__":
    main()
