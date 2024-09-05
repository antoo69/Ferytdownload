from pyrogram import Client, filters
from pyrogram.types import Message
import os
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, BLACKLIST_FILE, ACTIVE_GROUPS_FILE
from datetime import datetime, timedelta

app = Client("antigcast_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load blacklist from file
def load_blacklist():
    try:
        with open(BLACKLIST_FILE, 'r') as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

blacklist = load_blacklist()
active_groups = {}

# Load active groups from file
def load_active_groups():
    try:
        with open(ACTIVE_GROUPS_FILE, 'r') as f:
            for line in f:
                group_id, expiry_date = line.strip().split(',')
                active_groups[int(group_id)] = datetime.strptime(expiry_date, "%Y-%m-%d")
    except FileNotFoundError:
        pass

load_active_groups()

# Save active groups to file
def save_active_groups():
    with open(ACTIVE_GROUPS_FILE, 'w') as f:
        for group_id, expiry_date in active_groups.items():
            f.write(f"{group_id},{expiry_date.strftime('%Y-%m-%d')}\n")

# 👮🏻‍♀️ PERINTAH ADMIN
@app.on_message(filters.command("addbl") & filters.user(OWNER_ID))
async def add_to_blacklist(client, message: Message):
    word = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else message.reply_to_message.text
    if word:
        with open(BLACKLIST_FILE, 'a') as f:
            f.write(f"{word}\n")
        blacklist.add(word)
        await message.reply(f"'{word}' telah ditambahkan ke blacklist.")
    else:
        await message.reply("Gunakan perintah dengan reply atau tambahkan text!")

@app.on_message(filters.command("deldbl") & filters.user(OWNER_ID))
async def remove_from_blacklist(client, message: Message):
    word = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else message.reply_to_message.text
    if word in blacklist:
        blacklist.remove(word)
        with open(BLACKLIST_FILE, 'w') as f:
            for item in blacklist:
                f.write(f"{item}\n")
        await message.reply(f"'{word}' telah dihapus dari blacklist.")
    else:
        await message.reply("Kata tidak ditemukan dalam blacklist.")

active = True

@app.on_message(filters.command("protect") & filters.user(OWNER_ID))
async def toggle_protection(client, message: Message):
    global active
    command = message.text.split()[1] if len(message.text.split()) > 1 else ""
    if command == "on":
        active = True
        await message.reply("Bot diaktifkan.")
    elif command == "off":
        active = False
        await message.reply("Bot dinonaktifkan.")
    else:
        await message.reply("Gunakan perintah yang valid: /protect [on|off]")

@app.on_message(filters.command("status") & filters.chat_type.groups)
async def status(client, message: Message):
    if active:
        await message.reply("Bot aktif.")
    else:
        await message.reply("Bot tidak aktif.")

# 🧑🏻‍💻 PERINTAH OWNER
@app.on_message(filters.command("add") & filters.user(OWNER_ID))
async def add_group(client, message: Message):
    try:
        group_id, duration = map(int, message.text.split()[1:3])
        expiry_date = datetime.now() + timedelta(days=duration)
        active_groups[group_id] = expiry_date
        save_active_groups()
        await message.reply(f"Bot diaktifkan di grup {group_id} selama {duration} hari.")
    except (ValueError, IndexError):
        await message.reply("Penggunaan: /add [Group ID] [Durasi (Hari)]")

@app.on_message(filters.command("addgc") & filters.user(OWNER_ID) & filters.chat_type.groups)
async def add_current_group(client, message: Message):
    try:
        duration = int(message.text.split()[1])
        group_id = message.chat.id
        expiry_date = datetime.now() + timedelta(days=duration)
        active_groups[group_id] = expiry_date
        save_active_groups()
        await message.reply(f"Bot diaktifkan di grup ini selama {duration} hari.")
    except (ValueError, IndexError):
        await message.reply("Penggunaan: /addgc [Durasi (Hari)]")

@app.on_message(filters.command("rmgc") & filters.user(OWNER_ID))
async def remove_group(client, message: Message):
    try:
        group_id = int(message.text.split()[1])
        if group_id in active_groups:
            del active_groups[group_id]
            save_active_groups()
            await message.reply(f"Grup {group_id} telah dihapus dari daftar grup aktif.")
        else:
            await message.reply(f"Grup {group_id} tidak ditemukan dalam daftar grup aktif.")
    except (ValueError, IndexError):
        await message.reply("Penggunaan: /rmgc [Group ID]")

@app.on_message(filters.command("groups") & filters.user(OWNER_ID))
async def list_active_groups(client, message: Message):
    if active_groups:
        groups_list = "\n".join([f"{group_id} - Aktif hingga {expiry_date.strftime('%Y-%m-%d')}" for group_id, expiry_date in active_groups.items()])
        await message.reply(f"Daftar grup aktif:\n{groups_list}")
    else:
        await message.reply("Tidak ada grup aktif.")

global_blacklist = set()

@app.on_message(filters.command("bl") & filters.user(OWNER_ID))
async def global_blacklist_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.text.split()[1])
    global_blacklist.add(user_id)
    await message.reply(f"User {user_id} telah di-blacklist secara global.")

@app.on_message(filters.command("unbl") & filters.user(OWNER_ID))
async def global_unblacklist_user(client, message: Message):
    user_id = message.reply_to_message.from_user.id if message.reply_to_message else int(message.text.split()[1])
    if user_id in global_blacklist:
        global_blacklist.remove(user_id)
        await message.reply(f"User {user_id} telah dihapus dari global blacklist.")
    else:
        await message.reply(f"User {user_id} tidak ditemukan dalam global blacklist.")

@app.on_message(filters.command("blist") & filters.user(OWNER_ID))
async def show_global_blacklist(client, message: Message):
    if global_blacklist:
        bl_list = "\n".join([str(user_id) for user_id in global_blacklist])
        await message.reply(f"Daftar global blacklist:\n{bl_list}")
    else:
        await message.reply("Global blacklist kosong.")

# Jalankan bot
if __name__ == "__main__":
    app.run()
