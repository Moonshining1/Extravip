import asyncio
from pyrogram import filters
from pyrogram.types import MessageEntity

from VIPMUSIC import app, LOGGER, HELPABLE
from VIPMUSIC.utils.database import add_lock, remove_lock, is_locked

# Define the types of locks and their corresponding filters
LOCK_TYPES = {
    'sticker': filters.sticker,
    'audio': filters.audio,
    'voice': filters.voice,
    'document': filters.document,
    'video': filters.video,
    'contact': filters.contact,
    'photo': filters.photo,
    'gif': filters.document & filters.mime_type("video/mp4"),
    'url': filters.entity(MessageEntity.URL) | filters.caption_entity(MessageEntity.URL),
    'bots': filters.status_update.new_chat_members,
    'forward': filters.forwarded,
    'game': filters.game,
    'location': filters.location,
}

# Command to lock a specific type
@app.on_message(filters.command(["lock"]) & filters.user(Config.SUDO_USERS))
async def lock_content(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please specify what you want to lock.")
        return

    lock_type = message.command[1]
    if lock_type in LOCK_TYPES:
        await add_lock(message.chat.id, lock_type)
        await message.reply_text(f"Locked {lock_type} in this chat.")
    else:
        await message.reply_text("Invalid lock type.")

# Command to unlock a specific type
@app.on_message(filters.command(["unlock"]) & filters.user(Config.SUDO_USERS))
async def unlock_content(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please specify what you want to unlock.")
        return

    lock_type = message.command[1]
    if lock_type in LOCK_TYPES:
        await remove_lock(message.chat.id, lock_type)
        await message.reply_text(f"Unlocked {lock_type} in this chat.")
    else:
        await message.reply_text("Invalid lock type.")

# Filter to check if a message should be blocked
@app.on_message(filters.group & filters.incoming)
async def block_locked_content(client, message):
    for lock_type, lock_filter in LOCK_TYPES.items():
        if await is_locked(message.chat.id, lock_type) and lock_filter(message):
            await message.delete()
            await message.reply_text(f"Content type {lock_type} is locked in this chat.")
            break

HELPABLE["lock"] = {
    "lock": "Lock certain content types in the chat.",
    "unlock": "Unlock certain content types in the chat.",
}
