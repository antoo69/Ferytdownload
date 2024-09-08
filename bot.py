from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config import TELEGRAM_BOT_TOKEN, TELEGRAPH_MEDIA_URL
from yt_dlp import YoutubeDL

# Fungsi untuk mengunduh video dengan resolusi yang dipilih
def download_youtube_video(url: str, resolution: str):
    ydl_opts = {
        'format': f'bestvideo[height<={resolution}]+bestaudio/best',  # Mendukung resolusi sesuai pilihan
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Lokasi dan nama file output
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',  # Mengonversi ke format MP4
        }],
        'cookiefile': 'path/to/cookies.txt'  # Jika menggunakan cookies, tambahkan di sini
    }

    with YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)

# Fungsi untuk mengirim media dari Telegraph sebelum menu lainnya
async def start(update: Update, context):
    # Kirim media sambutan dari Telegraph
    await context.bot.send_photo(chat_id=update.effective_chat.id, photo=TELEGRAPH_MEDIA_URL)

    # Membuat tombol inline untuk memilih resolusi
    keyboard = [
        [InlineKeyboardButton("360p", callback_data='360')],
        [InlineKeyboardButton("480p", callback_data='480')],
        [InlineKeyboardButton("720p", callback_data='720')],
        [InlineKeyboardButton("1080p", callback_data='1080')],
        [InlineKeyboardButton("4K", callback_data='2160')],
        [InlineKeyboardButton("Tentang Bot", callback_data='about_bot')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Kirim pesan dengan tombol inline
    await update.message.reply_text(
        "Selamat datang di YouTube Downloader Bot!\n"
        "Bot ini dibuat oleh @fsyrl.\n"
        "Silakan pilih resolusi video yang ingin Anda unduh:",
        reply_markup=reply_markup
    )

# Handler untuk pilihan tombol inline
async def button_handler(update: Update, context):
    query = update.callback_query
    await query.answer()

    if query.data == 'about_bot':
        await query.edit_message_text(text="Bot ini dibuat oleh @fsyrl untuk mengunduh video YouTube hingga kualitas 4K.")
        return

    # Resolusi yang dipilih
    resolution = query.data

    # Kirim pesan untuk meminta tautan YouTube
    await query.edit_message_text(text=f"Anda memilih resolusi {resolution}p.\nSilakan kirim tautan YouTube yang ingin diunduh.")

    # Simpan resolusi dalam data kontekstual pengguna
    context.user_data['resolution'] = resolution

# Fungsi untuk menangani pesan berisi tautan YouTube
async def handle_message(update: Update, context):
    url = update.message.text
    resolution = context.user_data.get('resolution', '1080')  # Default ke 1080p jika tidak ada pilihan

    await update.message.reply_text(f"Mengunduh video dari: {url} dengan resolusi {resolution}p...")

    # Proses unduhan
    try:
        file_path = download_youtube_video(url, resolution)
        await update.message.reply_text(f"Unduhan selesai! Mengirim file...")
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))
    except Exception as e:
        await update.message.reply_text(f"Terjadi kesalahan saat mengunduh: {str(e)}")

# Fungsi utama untuk menjalankan bot
if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Command handler
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Mulai polling
    application.run_polling()
