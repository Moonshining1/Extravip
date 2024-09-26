import asyncio
import importlib
import requests  # Ensure requests is installed

from pyrogram import filters
from pyrogram import idle
from pyrogram.types import Message

import config
from config import BANNED_USERS
from VIPMUSIC import HELPABLE, LOGGER, app, userbot
from VIPMUSIC.core.call import VIP
from VIPMUSIC.plugins import ALL_MODULES
from VIPMUSIC.utils.database import get_banned_users, get_gbanned

# Function to get live cricket scores (using a placeholder API)
def get_live_cricket_score():
    try:
        # Replace this URL with a real cricket score API endpoint
        response = requests.get("https://api.cricapi.com/v1/currentMatches?apikey=6909402640:AAErcuUlvVxg7NNbLT-_5SD1j90GkLqVpwE")
        data = response.json()

        if 'matches' in data:
            scores = []
            for match in data['matches']:
                team1 = match['team1']['name']
                team2 = match['team2']['name']
                score1 = match['team1']['score']
                score2 = match['team2']['score']
                scores.append(f"{team1} {score1} vs {team2} {score2}")
            return "\n".join(scores) if scores else "No live matches at the moment."
        else:
            return "Unable to fetch cricket scores."
    except Exception as e:
        LOGGER.error(f"Error fetching live cricket scores: {e}")
        return "An error occurred while fetching the scores."

# Command handler for /cs
@app.on_message(filters.command("cs") & ~filters.user(BANNED_USERS))
async def cricket_score(_, message: Message):
    # Send typing action
    await message.reply_text("Fetching live cricket scores...")

    # Get live cricket scores
    scores = get_live_cricket_score()

    # Send the scores back to the user
    await message.reply_text(scores)

# Main function to start the bot
if __name__ == "__main__":
    app.start()
    LOGGER.info("Bot is running...")
    idle()
