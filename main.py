import os
import subprocess
import git
from pyrogram import Client, filters
from pyrogram.types import Message
from config import BOT_TOKEN, API_ID, API_HASH

# Directory to clone and run repositories
DEPLOY_DIR = "deploy_repos"

# Create directory if it doesn't exist
if not os.path.exists(DEPLOY_DIR):
    os.makedirs(DEPLOY_DIR)

# Initialize the Pyrogram Client
app = Client("bot_maker", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# To store running processes (up to 3 repositories)
running_bots = []

MAX_BOTS = 3


@app.on_message(filters.command("start"))
async def start(client: Client, message: Message):
    """Start command to welcome the user."""
    await message.reply("Welcome to the Bot Maker! Send me a GitHub repo link to deploy a Telegram bot.")


@app.on_message(filters.text & ~filters.edited)
async def deploy_bot(client: Client, message: Message):
    """Deploy bot from GitHub repository link."""
    global running_bots
    repo_url = message.text.strip()

    if "github.com" not in repo_url:
        await message.reply("Please send a valid GitHub repository URL.")
        return

    if len(running_bots) >= MAX_BOTS:
        await message.reply(f"Maximum number of running bots reached ({MAX_BOTS}). Stop one before deploying more.")
        return

    # Parse the repository name from the URL
    repo_name = repo_url.split('/')[-1].replace('.git', '')
    repo_path = os.path.join(DEPLOY_DIR, repo_name)

    # Clone or update the repository
    if not os.path.exists(repo_path):
        await message.reply(f"Cloning repository {repo_name}...")
        git.Repo.clone_from(repo_url, repo_path)
    else:
        await message.reply(f"Updating repository {repo_name}...")
        repo = git.Repo(repo_path)
        repo.git.pull()

    # Install dependencies (assuming Python project)
    await message.reply(f"Installing dependencies for {repo_name}...")
    subprocess.run(["pip", "install", "-r", os.path.join(repo_path, "requirements.txt")])

    # Run the bot (assuming main bot script is `bot.py`)
    await message.reply(f"Running bot from {repo_name}...")
    process = subprocess.Popen(["python3", os.path.join(repo_path, "bot.py")])

    # Save running process info
    running_bots.append((repo_name, process))
    await message.reply(f"Bot {repo_name} is now running.")

@app.on_message(filters.command("stop"))
async def stop_bot(client: Client, message: Message):
    """Stop a specific running bot."""
    global running_bots
    bot_name = message.text.strip().split()[-1]

    for i, (name, process) in enumerate(running_bots):
        if name == bot_name:
            process.terminate()
            running_bots.pop(i)
            await message.reply(f"Bot {bot_name} stopped.")
            return

    await message.reply(f"No running bot found with name {bot_name}.")


@app.on_message(filters.command("list"))
async def list_bots(client: Client, message: Message):
    """List all running bots."""
    if not running_bots:
        await message.reply("No bots are currently running.")
    else:
        running_bot_names = [name for name, _ in running_bots]
        await message.reply(f"Running bots: {', '.join(running_bot_names)}")


if __name__ == "__main__":
    app.run()
