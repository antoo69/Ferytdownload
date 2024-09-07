from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import add_user_to_blacklist, remove_user_from_blacklist, get_blacklisted_users, add_group, remove_group, get_active_groups
from schedule import schedule_bot
from config import Config

@Client.on_message(filters.command("start"))
async def start(client, message):
    buttons = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Support Channel", url=Config.SUPPORT_CHANNEL)],
            [InlineKeyboardButton("Support Group", url=Config.SUPPORT_GROUP)],
            [InlineKeyboardButton("Owner", url=f"https://t.me/{Config.OWNER_USERNAME}")],
            [InlineKeyboardButton("Tambahkan pada Group", url=f"https://t.me/{client.me.username}?startgroup=true")]
        ]
    )
    
    await client.send_photo(
        chat_id=message.chat.id,
        photo=Config.LOGO_URL,
        caption=f"Selamat datang di bot Anti Gcast! Bot ini dibuat oleh @fsyrl.\n\nGunakan tombol di bawah ini untuk mengakses dukungan.",
        reply_markup=buttons
    )

@Client.on_message(filters.command("add"))
async def add_group_cmd(client, message):
    if len(message.command) < 3:
        await message.reply("Format salah! Gunakan: /add [Group ID] [Durasi]")
        return
    group_id = int(message.command[1])
    duration = int(message.command[2])
    await schedule_bot(client, group_id, duration)

@Client.on_message(filters.command("addgc"))
async def add_group_current(client, message):
    if len(message.command) < 2:
        await message.reply("Format salah! Gunakan: /addgc [Durasi]")
        return
    duration = int(message.command[1])
    await schedule_bot(client, message.chat.id, duration)

@Client.on_message(filters.command("rmgc"))
async def remove_group_cmd(client, message):
    group_id = int(message.command[1])
    remove_group(group_id)
    await message.reply(f"Group {group_id} telah dihapus dari daftar aktif.")

@Client.on_message(filters.command("groups"))
async def list_groups(client, message):
    groups = get_active_groups()
    group_list = "\n".join([str(group['group_id']) for group in groups])
    await message.reply(f"Daftar group aktif:\n{group_list}")

@Client.on_message(filters.command("bl"))
async def add_user_blacklist(client, message):
    user_id = message.reply_to_message.from_user.id
    add_user_to_blacklist(user_id)
    await message.reply(f"User {user_id} telah ditambahkan ke blacklist global.")

@Client.on_message(filters.command("unbl"))
async def remove_user_blacklist(client, message):
    user_id = message.reply_to_message.from_user.id
    remove_user_from_blacklist(user_id)
    await message.reply(f"User {user_id} telah dihapus dari blacklist global.")

@Client.on_message(filters.command("blist"))
async def list_blacklisted_users(client, message):
    users = get_blacklisted_users()
    user_list = "\n".join([str(user['user_id']) for user in users])
    await message.reply(f"Daftar user blacklist:\n{user_list}")
