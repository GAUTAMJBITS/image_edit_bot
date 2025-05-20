import os
from datetime import time as dt_time
import time

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from image_utils import resize_image, compress_image


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Send me an image and use /resize or /compress after that.")


async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Get the highest resolution photo
        photo = update.message.photo[-1]
        file = await photo.get_file()

        # Generate a unique filename using user ID and timestamp
        user_id = update.effective_user.id
        timestamp = int(time.time())
        input_path = f"{user_id}_{timestamp}_input.jpg"

        # Download the image
        await file.download_to_drive(input_path)

        # Store path in user_data for later use (resize/compress)
        context.user_data['input_path'] = input_path

        await update.message.reply_text(
            "✅ Image received!\n\nNow send a command:\n"
            "`/resize <width> <height>`\n"
            "or\n"
            "`/compress <quality>` (1-100)\n\n"
            "Example:\n`/resize 400 300`\n`/compress 70`",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to process the image.\nError: {e}")


async def resize_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        width = int(context.args[0])
        height = int(context.args[1])
        input_path = context.user_data.get('input_path', 'input.jpg')
        output_path = "resized.jpg"
        resize_image(input_path, output_path, width, height)
        await update.message.reply_photo(photo=open(output_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


async def compress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        quality = int(context.args[0])
        input_path = context.user_data.get('input_path', 'input.jpg')
        output_path = "compressed.jpg"
        compress_image(input_path, output_path, quality)
        await update.message.reply_photo(photo=open(output_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")


if __name__ == '__main__':
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("resize", resize_command))
    app.add_handler(CommandHandler("compress", compress_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))

    print("Bot is running...")
    app.run_polling()
