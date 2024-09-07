from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors.rpcerrorlist import FloodWaitError
from scrapers import Item,get_new_updates
import asyncio
import random
import logging
from urllib.parse import urlparse
import os

logging.basicConfig(filename="app.log",encoding='utf-8',format="{asctime} - {message}",style="{")
logger = logging.getLogger("telegram_bot")
logger.setLevel(logging.INFO)

api_id = os.getenv("api_id")#"1813834"
api_hash = os.getenv("api_hash")#"567770705143bc5db93174935d80190c"
secret_session = os.getenv("session_string")

client = TelegramClient(StringSession(secret_session),api_id,api_hash,request_retries=2)

async def telegram_notifier(X:dict[Item]):
    peer_id = await client.get_peer_id('https://t.me/+suTl5roT8nNlODI0')
    for x in X:
        try:
            msg = await client.send_message(peer_id,X[x].message_text,parse_mode="MD",link_preview=True)
        except FloodWaitError:
            logger.info(FloodWaitError.message)
            
        logger.info(f'{urlparse(X[x].link).netloc}: a message has been sent for {X[x].__str__()} with id:{msg.id}')
        await asyncio.sleep(random.uniform(10,30)+15)
    
with client:
    new_items = get_new_updates(db_name="namshi")
    client.loop.run_until_complete(telegram_notifier(new_items))