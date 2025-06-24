# scripts/telegram_scraper.py

import os
import pandas as pd
from dotenv import load_dotenv
from telethon import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest

# Load environment variables
load_dotenv()

api_id = int(os.getenv("TELEGRAM_API_ID"))
api_hash = os.getenv("TELEGRAM_API_HASH")
phone = os.getenv("TELEGRAM_PHONE")

# Set up Telethon client
client = TelegramClient("ethio_session", api_id, api_hash)

# ✅ ASYNC function for use in notebooks
async def fetch_messages_async(channel_username, limit=300):
    await client.start(phone=phone)
    channel = await client.get_entity(channel_username)
    result = await client(GetHistoryRequest(
        peer=channel,
        limit=limit,
        offset_date=None,
        offset_id=0,
        max_id=0,
        min_id=0,
        add_offset=0,
        hash=0
    ))
    messages = result.messages
    data = []
    for msg in messages:
        if msg.message:
            data.append({
                "channel": channel_username,
                "id": msg.id,
                "date": msg.date,
                "text": msg.message,
                "views": msg.views if hasattr(msg, 'views') else None,
                "media": bool(msg.media)
            })
    return pd.DataFrame(data)

# ✅ Optional sync wrapper for .py scripts
def fetch_messages(channel_username, limit=300):
    import nest_asyncio, asyncio
    nest_asyncio.apply()
    return asyncio.run(fetch_messages_async(channel_username, limit))
