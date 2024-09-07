import os

class Config:
    API_ID = os.getenv("API_ID")
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    MONGO_URI = os.getenv("MONGO_URI")
    OWNER_ID = int(os.getenv("OWNER_ID"))  # ID Telegram Owner
    LOGO_URL = os.getenv("LOGO_URL")  # URL untuk gambar logo
    SUPPORT_CHANNEL = os.getenv("SUPPORT_CHANNEL")  # URL support channel
    SUPPORT_GROUP = os.getenv("SUPPORT_GROUP")  # URL support group
    OWNER_USERNAME = os.getenv("OWNER_USERNAME")  # Username Telegram owner
