import os

# Path tempat menyimpan file userbot
CONFIG_PATH = "./userbot_configs/"

@bot.on_message(filters.text & filters.private)
async def handle_user_input(client, message):
    # Asumsi pesan kedua adalah API ID
    if message.text.isdigit():
        api_id = message.text
        await message.reply("Sekarang kirimkan API Hash Anda.")
        
        # Simpan API ID ke file
        with open(os.path.join(CONFIG_PATH, f"{message.from_user.id}_config.ini"), "w") as config_file:
            config_file.write(f"api_id={api_id}\n")
    
    # Jika ini adalah API Hash
    elif len(message.text) == 32:
        api_hash = message.text
        await message.reply("Userbot berhasil dibuat! Anda sekarang bisa menjalankan userbot Anda.")
        
        # Tambahkan API Hash ke file
        with open(os.path.join(CONFIG_PATH, f"{message.from_user.id}_config.ini"), "a") as config_file:
            config_file.write(f"api_hash={api_hash}\n")

        # Jalankan proses untuk menjalankan userbot
        # Os.system atau subprocess untuk menjalankan command
