from pyrogram import Client
from config import Config
import anti_gcast
import commands

app = Client("anti_gcast_bot", api_id=Config.API_ID, api_hash=Config.API_HASH, bot_token=Config.BOT_TOKEN)

if __name__ == "__main__":
    app.run()
