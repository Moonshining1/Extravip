import requests
import random
import re
from MukeshAPI import api
from pyrogram import filters
from pyrogram.enums import ChatAction
from VIPMUSIC import app

# List of random emojis for reactions
EMOJI_LIST = ["😃", "😂", "👍", "🔥", "😎", "🤔", "😍", "😅", "🤖", "🎉", "💯", "🕊️","🐋"]

# Function to send a random emoji reaction
async def react_with_random_emoji(client, message):
    emoji = random.choice(EMOJI_LIST)
    await app.send_reaction(message.chat.id, message.id, emoji)

