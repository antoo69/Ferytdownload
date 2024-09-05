import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

# Files for storing blacklist and active groups
BLACKLIST_FILE = os.getenv("BLACKLIST_FILE", "blacklist.txt")
ACTIVE_GROUPS_FILE = os.getenv("ACTIVE_GROUPS_FILE", "active_groups.json")

# Other configurations
DEBUG = bool(os.getenv("DEBUG", "False"))
