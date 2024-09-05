import os
from dotenv import load_dotenv

# Memuat file .env
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))
BLACKLIST_FILE = os.getenv("BLACKLIST_FILE", "blacklist.txt")
ACTIVE_GROUPS_FILE = os.getenv("ACTIVE_GROUPS_FILE", "active_groups.txt")
