import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from PIL import Image

TOKEN = os.environ.get("BOT_TOKEN")  # Railway injects this from dashboard

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Send an image, then use /resize width height or /compress quality.")

async def handle_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    input_path = "input.jpg"
    await file.download_to_drive(input_path)
    context.user_data["input_path"] = input_path
    await update.message.reply_text("Image received. Now use /resize or /compress.")

async def resize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_path = context.user_data.get("input_path")
        width = int(context.args[0])
        height = int(context.args[1])
        img = Image.open(input_path)
        img = img.resize((width, height))
        img.save("resized.jpg")
        await update.message.reply_photo(photo=open("resized.jpg", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def compress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        input_path = context.user_data.get("input_path")
        quality = int(context.args[0])
        img = Image.open(input_path)
        img.save("compressed.jpg", quality=quality)
        await update.message.reply_photo(photo=open("compressed.jpg", "rb"))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("resize", resize))
    app.add_handler(CommandHandler("compress", compress))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image))
    print("Bot running...")
    app.run_polling()
