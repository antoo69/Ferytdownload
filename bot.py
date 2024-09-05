from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, BLACKLIST_FILE, ACTIVE_GROUPS_FILE
import json

app = Client("AntiGcastBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Load blacklist and active groups from file
def load_blacklist():
    try:
        with open(BLACKLIST_FILE, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def save_blacklist(blacklist):
    with open(BLACKLIST_FILE, 'w') as f:
        f.write('\n'.join(blacklist))

def load_active_groups():
    try:
        with open(ACTIVE_GROUPS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_active_groups(groups):
    with open(ACTIVE_GROUPS_FILE, 'w') as f:
        json.dump(groups, f)

blacklist = load_blacklist()
active_groups = load_active_groups()

@app.on_message(filters.command("start"))
def start(client, message: Message):
    message.reply("Bot has started!")

# Define additional command handlers based on your requirements

if __name__ == "__main__":
    app.run()
