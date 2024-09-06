from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# Telegram Bot API credentials
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
