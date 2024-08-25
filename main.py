from telethon import TelegramClient
from scrapers import Item,get_new_updates
import asyncio
import random

api_id = "1813834"
api_hash = "567770705143bc5db93174935d80190c"

client = TelegramClient('anon',api_id,api_hash,proxy=("socks5",'127.0.0.1',8086),request_retries=2)

async def namshi_notifier(X:dict[Item]):
    peer_id = await client.get_peer_id('https://t.me/+suTl5roT8nNlODI0')
    for x in X:
        msg = f"**{X[x].name}**\n Price: {X[x].price}\n [CLICK HERE]({X[x].link})"
        await client.send_message(peer_id,msg,parse_mode="MD",link_preview=True)
        await asyncio.sleep(random.uniform(1,5))

async def main():
    #send some msg to notifier channel
    peer_id = await client.get_peer_id('https://t.me/+suTl5roT8nNlODI0')
    await client.send_message(peer_id,"Hello,World!")
    
with client:
    new_items = get_new_updates()
    client.loop.run_until_complete(namshi_notifier(new_items))