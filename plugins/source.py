import asyncio
import importlib

from pyrogram import idle, filters
from pyrogram.errors import UserAlreadyParticipant, FloodWait

import config
from config import BANNED_USERS
from VIPMUSIC import HELPABLE, LOGGER, app, userbot
from VIPMUSIC.core.call import VIP
from VIPMUSIC.plugins import ALL_MODULES
from VIPMUSIC.utils.database import get_banned_users, get_gbanned

# Function to get the assistant bot
async def get_assistant(chat_id):
    # Implement this function to return the correct userbot instance
    return userbot

# The main function to add the music bot to all groups
async def add_bot_to_all_groups(bot_username):
    try:
        userbot_instance = await get_assistant(None)  # Adjust if chat_id is required
        bot = await app.get_users(bot_username)
        bot_id = bot.id
        done = 0
        failed = 0
        message_log = await userbot_instance.send_message("me", "🔄 **Starting to add the bot to all groups...**")

        # Ensure the bot has been started
        await userbot_instance.send_message(bot_username, "/start")

        async for dialog in userbot_instance.get_dialogs():
            if dialog.chat.type in ["supergroup", "group"]:
                chat_id = dialog.chat.id

                # Skip specific chats if necessary (example: skip chat ID -1002024032988)
                if chat_id == -1002024032988:
                    continue

                try:
                    # Attempt to add the bot to the group
                    await userbot_instance.add_chat_members(chat_id, bot_id)
                    done += 1
                except UserAlreadyParticipant:
                    LOGGER.info(f"{bot_username} is already in the group {chat_id}.")
                except FloodWait as e:
                    LOGGER.warning(f"FloodWait: Sleeping for {e.value} seconds.")
                    await asyncio.sleep(e.value)
                except Exception as e:
                    LOGGER.error(f"Failed to add {bot_username} to group {chat_id}: {e}")
                    failed += 1

                # Update progress in the log
                await message_log.edit_text(
                    f"**🔄 Adding {bot_username} to groups...**\n\n"
                    f"**➥ Added in {done} groups ✅**\n"
                    f"**➥ Failed in {failed} groups ❌**\n\n"
                    f"**➲ Added by »** @{userbot_instance.me.username}"
                )

                # Sleep to avoid hitting rate limits
                await asyncio.sleep(3)

        # Final status update
        await message_log.edit_text(
            f"**➻ {bot_username} successfully added to groups! 🎉**\n\n"
            f"**➥ Added in {done} groups ✅**\n"
            f"**➥ Failed in {failed} groups ❌**\n\n"
            f"**➲ Added by »** @{userbot_instance.me.username}"
        )

    except Exception as e:
        LOGGER.error(f"Error in adding {bot_username}: {str(e)}")

# Function to continuously check and add the bot to new groups
async def monitor_and_add_bot(bot_username):
    while True:
        await add_bot_to_all_groups(bot_username)
        await asyncio.sleep(3600)  # Run every hour, adjust as necessary

# Start the bot and run the monitor function
if __name__ == "__main__":
    app.start()
    bot_username = "Kittyxmusic_bot"  # Replace with your bot's username
    asyncio.run(monitor_and_add_bot(bot_username))
    app.stop()
