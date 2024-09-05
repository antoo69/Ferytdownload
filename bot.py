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

def is_owner(user_id):
    return user_id == OWNER_ID

def is_protected(chat_id):
    return active_groups.get(str(chat_id), {}).get('protected', False)

@app.on_message(filters.command("addbl") & filters.user(OWNER_ID))
def add_to_blacklist(client, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = " ".join(message.command[1:])
    
    if text:
        blacklist.add(text)
        save_blacklist(blacklist)
        message.reply(f"Added to blacklist: {text}")
    else:
        message.reply("No text provided to blacklist.")

@app.on_message(filters.command("deldbl") & filters.user(OWNER_ID))
def remove_from_blacklist(client, message: Message):
    if message.reply_to_message:
        text = message.reply_to_message.text
    else:
        text = " ".join(message.command[1:])
    
    if text in blacklist:
        blacklist.remove(text)
        save_blacklist(blacklist)
        message.reply(f"Removed from blacklist: {text}")
    else:
        message.reply("Text not found in blacklist.")

@app.on_message(filters.command("protect") & filters.user(OWNER_ID))
def toggle_protect(client, message: Message):
    status = message.command[1].lower() if len(message.command) > 1 else None
    chat_id = message.chat.id

    if status not in ["on", "off"]:
        message.reply("Usage: /protect [on|off]")
        return

    is_protected_status = status == "on"
    active_groups[str(chat_id)] = {"protected": is_protected_status}
    save_active_groups(active_groups)
    
    message.reply(f"Bot protection is now {'enabled' if is_protected_status else 'disabled'}.")

@app.on_message(filters.command("status") & filters.chat_type.groups)
def status(client, message: Message):
    chat_id = message.chat.id
    protected_status = is_protected(chat_id)
    message.reply(f"Bot protection status: {'Enabled' if protected_status else 'Disabled'}")

@app.on_message(filters.command("add") & filters.user(OWNER_ID))
def add_group(client, message: Message):
    if len(message.command) != 3:
        message.reply("Usage: /add [Group ID] [Duration (Days)]")
        return
    
    group_id = message.command[1]
    duration = int(message.command[2])
    active_groups[group_id] = {"expires": duration}
    save_active_groups(active_groups)
    
    message.reply(f"Group {group_id} has been activated for {duration} days.")

@app.on_message(filters.command("addgc") & filters.chat_type.groups)
def add_group_from_chat(client, message: Message):
    if len(message.command) != 2:
        message.reply("Usage: /addgc [Duration (Days)]")
        return
    
    duration = int(message.command[1])
    group_id = str(message.chat.id)
    active_groups[group_id] = {"expires": duration}
    save_active_groups(active_groups)
    
    message.reply(f"Group {group_id} has been activated for {duration} days.")

@app.on_message(filters.command("rmgc") & filters.user(OWNER_ID))
def remove_group(client, message: Message):
    if len(message.command) != 2:
        message.reply("Usage: /rmgc [Group ID]")
        return
    
    group_id = message.command[1]
    if group_id in active_groups:
        del active_groups[group_id]
        save_active_groups(active_groups)
        message.reply(f"Group {group_id} has been removed from active groups.")
    else:
        message.reply("Group ID not found.")

@app.on_message(filters.command("groups") & filters.user(OWNER_ID))
def list_active_groups(client, message: Message):
    if not active_groups:
        message.reply("No active groups.")
        return
    
    response = "Active Groups:\n"
    for group_id, info in active_groups.items():
        response += f"Group ID: {group_id}, Duration: {info['expires']} days\n"
    
    message.reply(response)

@app.on_message(filters.command("bl") & filters.user(OWNER_ID))
def blacklist_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.command[1] if len(message.command) > 1 else None
    
    if user_id:
        # You need to implement how to globally blacklist users
        message.reply(f"User {user_id} has been added to the global blacklist.")
    else:
        message.reply("No user ID provided.")

@app.on_message(filters.command("unbl") & filters.user(OWNER_ID))
def unblacklist_user(client, message: Message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.command[1] if len(message.command) > 1 else None
    
    if user_id:
        # You need to implement how to globally unblacklist users
        message.reply(f"User {user_id} has been removed from the global blacklist.")
    else:
        message.reply("No user ID provided.")

@app.on_message(filters.command("blist") & filters.user(OWNER_ID))
def list_blacklist(client, message: Message):
    if not blacklist:
        message.reply("Blacklist is empty.")
        return
    
    response = "Global Blacklist:\n"
    response += "\n".join(blacklist)
    
    message.reply(response)

if __name__ == "__main__":
    app.run()
