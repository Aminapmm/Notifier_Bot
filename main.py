from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import FloodWaitError
from scrapers import Item,get_new_updates
import asyncio
import random
import logging
from urllib.parse import urlparse
import os
import sys

logging.basicConfig(filename="app.log",encoding='utf-8',format="{asctime} - {message}",style="{")
logger = logging.getLogger("telegram_bot")
logger.setLevel(logging.INFO)

api_id = os.getenv("api_id")
api_hash = os.getenv("api_hash")
session_string = os.getenv("session_string")
bot_token = os.getenv("bot_token")

client = TelegramClient(StringSession(session_string),api_id,api_hash,connection_retries=2,request_retries=2).start(bot_token=bot_token)

async def telegram_notifier(X:dict[Item]):
    for x in X:
        try:
            msg = await client.send_message(-1002175476647,X[x].msg,parse_mode="MD",link_preview=True)
            logger.info(f'{urlparse(X[x].link).netloc}: a message has been sent for {X[x].__str__()} with id:{msg.id}')

        except FloodWaitError as e:
            logger.info(FloodWaitError.message)
            return e.message
            
        await asyncio.sleep(random.uniform(10,20)+5)

    
with client:
    new_items = get_new_updates(db_name="namshi")
    client.loop.run_until_complete(telegram_notifier(new_items))