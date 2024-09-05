from pyrogram import Client, filters

# Inisialisasi Bot
api_id = "YOUR_API_ID"
api_hash = "YOUR_API_HASH"
bot_token = "YOUR_BOT_TOKEN"

bot = Client(
    "userbot_maker_bot",
    api_id=api_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Command untuk memulai bot
@bot.on_message(filters.command("start") & filters.private)
async def start_command(client, message):
    await message.reply("Selamat datang di Userbot Maker!\nKetik /buatuserbot untuk memulai membuat userbot.")

# Command untuk membuat userbot baru
@bot.on_message(filters.command("buatuserbot") & filters.private)
async def buat_userbot(client, message):
    await message.reply("Silakan kirimkan API ID dan API Hash Anda untuk memulai.")
    
    # Tambahkan proses untuk menyimpan informasi user dan mulai membuat userbot

bot.run()
