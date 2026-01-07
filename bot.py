import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
from utils import is_video_url, download

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# تحميل المتغيرات البيئية
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('أهلاً بك! أرسل لي رابط فيديو من (TikTok, Instagram, YouTube, Facebook) وسأقوم بتحميله لك بدون علامة مائية.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not is_video_url(url):
        return

    status_message = await update.message.reply_text('جاري معالجة الفيديو... يرجى الانتظار ⏳', quote=True)
    
    try:
        file_path = download(url)
        if file_path and os.path.exists(file_path):
            await update.message.reply_video(video=open(file_path, 'rb'), quote=True)
            os.remove(file_path) # حذف الملف بعد الإرسال لتوفير المساحة
            await status_message.delete()
        else:
            await status_message.edit_text('عذراً، تعذر تحميل الفيديو. تأكد من أن الرابط صحيح.')
    except Exception as e:
        logger.error(f"Error: {e}")
        await status_message.edit_text(f'حدث خطأ أثناء التحميل: {str(e)}')

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN is not set!")
        return

    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    (main) 
