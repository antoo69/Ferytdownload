# Anti Gcast Bot

Bot anti-gcast untuk Telegram dengan Pyrogram dan MongoDB.

## Fitur
- Mengelola blacklist kata-kata.
- Mengaktifkan dan menonaktifkan bot di grup.
- Pengaturan waktu penggunaan bot.
- Global blacklist user.
- Menampilkan gambar logo di `/start` dengan tombol navigasi.

## Pengaturan
1. Clone repository ini.
2. Install dependencies: `pip install -r requirements.txt`
3. Atur environment variables: 
   - `API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_URI`, `OWNER_ID`
   - `LOGO_URL`, `SUPPORT_CHANNEL`, `SUPPORT_GROUP`, `OWNER_USERNAME`
4. Jalankan bot: `python3 bot.py`

## Created by @fsyrl

## Deployment di VPS:
1. Install Python dan MongoDB di VPS.
2. Clone repository `git clone https://github.com/antoo69/builder`
3. Install dependencies: `pip install -r requirements.txt`
4. Atur environment variables di .env.
5. `cp .env config.env`
6. Jalankan bot: `python3 bot.py`
