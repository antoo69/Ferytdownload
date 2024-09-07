from pyrogram import Client, filters
from database import is_blacklisted, add_to_blacklist, remove_from_blacklist

@Client.on_message(filters.text)
async def check_gcast(client, message):
    if is_blacklisted(message.text):
        await message.delete()

@Client.on_message(filters.command("addbl") & filters.reply)
async def add_blacklist(client, message):
    word = message.reply_to_message.text
    add_to_blacklist(word)
    await message.reply(f"'{word}' telah ditambahkan ke blacklist.")

@Client.on_message(filters.command("deldbl") & filters.reply)
async def remove_blacklist(client, message):
    word = message.reply_to_message.text
    remove_from_blacklist(word)
    await message.reply(f"'{word}' telah dihapus dari blacklist.")
