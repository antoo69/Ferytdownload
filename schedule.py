import time
from pyrogram import Client
from database import add_group, remove_group

async def schedule_bot(client: Client, group_id, duration):
    add_group(group_id, duration)
    await client.send_message(group_id, f"Bot aktif selama {duration} hari.")
    
    time.sleep(duration * 86400)  # Convert days to seconds
    remove_group(group_id)
    await client.send_message(group_id, "Waktu habis! Bot telah dinonaktifkan.")
