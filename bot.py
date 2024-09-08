import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import yt_dlp
from config import TOKEN, ADMIN_ID, LOGO_PATH

# Konfigurasi logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Fungsi untuk memulai bot
async def start(update: Update, context):
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Download", callback_data='download')],
        [InlineKeyboardButton("Tentang Saya", callback_data='about')],
        [InlineKeyboardButton("Cara Pakai", callback_data='how_to_use')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if LOGO_PATH and os.path.isfile(LOGO_PATH):
        with open(LOGO_PATH, 'rb') as logo:
            await context.bot.send_photo(chat_id=update.effective_chat.id, photo=logo, caption="Selamat datang di bot downloader!", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Selamat datang di bot downloader! Pilih opsi di bawah.", reply_markup=reply_markup)

# Fungsi untuk menangani tombol inline
async def button(update: Update, context):
    query = update.callback_query
    data = query.data

    if data == 'download':
        await query.edit_message_text(text="Kirimkan saya URL YouTube.")
    elif data == 'about':
        await query.edit_message_text(text="Bot ini dibuat untuk mendownload video dari YouTube.")
    elif data == 'how_to_use':
        await query.edit_message_text(text="Kirimkan URL YouTube, lalu pilih resolusi video untuk didownload.")
    else:
        await query.answer()

# Fungsi untuk menangani pesan dengan URL
async def handle_message(update: Update, context):
    url = update.message.text
    context.user_data['url'] = url  # Simpan URL untuk penggunaan di callback

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])
        sorted_formats = sorted(formats, key=lambda x: x.get('height', 0))

        keyboard = [
            [InlineKeyboardButton(f"{f['height']}p", callback_data=f"download_{f['format_id']}")] for f in sorted_formats if 'height' in f
        ]
        keyboard.append([InlineKeyboardButton("Download MP3", callback_data='download_mp3')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("Silahkan pilih resolusi:", reply_markup=reply_markup)

# Fungsi untuk menangani tombol download
async def download_button(update: Update, context):
    query = update.callback_query
    data = query.data
    url = context.user_data.get('url')

    if not url:
        await query.answer("URL tidak ditemukan. Kirimkan URL terlebih dahulu.")
        return

    formats = data.split('_')
    format_type = formats[0] if len(formats) > 1 else None
    format_id = formats[1] if len(formats) > 1 else None

    ydl_opts = {
        'format': format_id if format_id else format_type,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'cookies': 'cookies.txt',
        'noplaylist': True,
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
            media_type = 'video' if format_id else 'audio'

            if media_type == 'video':
                with open(filename, 'rb') as f:
                    await context.bot.send_video(chat_id=update.effective_chat.id, video=f, caption=f"Video berhasil diunduh: {info_dict['title']}")
            else:
                with open(filename, 'rb') as f:
                    await context.bot.send_audio(chat_id=update.effective_chat.id, audio=f, caption=f"Audio berhasil diunduh: {info_dict['title']}")
    except Exception as e:
        logger.error(f"Error downloading video: {e}")
        await query.edit_message_text(text="Terjadi kesalahan saat mendownload video.")

# Fungsi untuk menghandle admin commands
async def user_count(update: Update, context):
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin.")
        return
    # Simulasi jumlah user, harus menggunakan penyimpanan yang lebih persisten
    user_count = len(context.bot_data.get('users', []))
    await update.message.reply_text(f"Jumlah pengguna: {user_count}")

async def broadcast(update: Update, context):
    if str(update.effective_user.id) != ADMIN_ID:
        await update.message.reply_text("Perintah ini hanya bisa digunakan oleh admin.")
        return

    if context.args:
        message = ' '.join(context.args)
        for user_id in context.bot_data.get('users', []):
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
            except Exception as e:
                logger.error(f"Error broadcasting message to {user_id}: {e}")
        await update.message.reply_text("Pesan berhasil dikirim ke semua pengguna.")
    else:
        await update.message.reply_text("Harap sertakan pesan yang ingin dikirim.")

# Fungsi utama
def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('user', user_count))
    application.add_handler(CommandHandler('broadcast', broadcast, filters=filters.Command() & filters.User(user_id=ADMIN_ID)))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_handler(CallbackQueryHandler(download_button, pattern='^download_'))

    application.run_polling()

if __name__ == '__main__':
    main()
