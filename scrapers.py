from bs4 import BeautifulSoup as bs
from requests import request
from datetime import datetime
import pickle
from urllib.parse import urljoin
import os
import time
import logging

logging.basicConfig(filename="app.log",encoding='utf-8',format="{asctime} - {message}",style="{")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Item:
    def __init__(self,base_url,properties:dict):
        
        self.link = properties['link']
        self.serial = properties['serial']
        self.timer = properties['timer']
        self.image = properties['image']
        self.price = properties['price']
        self.name = properties['name']
        self.date_updated = properties['date_updated']
        self.msg = properties['msg']
        
    def __str__(self):
        return f"{self.name}"
    
    def __eq__(self,other):
        return self.price == other.price

    def __ne__(self, other: object) -> bool:
        return self.price != other.price
    
    
def namshi_scraper():
    url = "https://www.namshi.com/uae-en/men-shoes-sports-trainers/?page=1&f%5Bbrand_code%5D=nike&f%5Bbrand_code%5D=under_armour&sort%5Bby%5D=discount_percent&sort%5Bdir%5D=desc"
    res = request("GET",url).content
    soup = bs(res,'lxml')
    items = soup.select(".ProductBox_container__wiajf .ProductBox_productBox__tPpGm")
    extracted_items = {}

    for item in items:

        properties = {}
        properties['link'] = urljoin("https://namshi.com",item['href'])
        properties['serial'] = item['href'].split("/")[3]
        properties['timer'] = item.find(class_="TimerSale_timer__321ZF")
        properties['image'] = list(map(lambda x:x.get('src'),item.find(class_="slider-list").find_all("img")))
        get_price = lambda price:price[1].text +" "+price[0].text
        properties['price'] = get_price(item.select((".ProductPrice_value__hnFSS,.ProductPrice_currency__issmK")))
        get_name = lambda name:name[0].text+"-"+name[1].text
        properties['name'] = get_name(item.select(".ProductBox_brand__oDc9f,.ProductBox_productTitle__6tQ3b"))
        properties['date_updated'] = time.time()
        properties['msg'] = f"{"Limited Offer" if properties['timer'] != None else ""}**{properties['name']}**\n Price: {properties['price']}\n [CLICK HERE]({properties['link']})"

        x = Item("https://namshi.com",properties)
        extracted_items[x.serial] = x
    
    return extracted_items

def sss_kuwait_scraper():
    pass

def export_to_file(items:dict,db_name='dbfile'):
    logging.info(f"{len(items)} new item saved to {db_name}")
    with open(f"db/{db_name}",'ab') as db_file:
        pickle.dump(items,db_file)

def load_db(db_file_name="dbfile"):#load db_file
    if os.path.exists(f"db/{db_file_name}"):
        with open(f"db/{db_file_name}",'rb') as db_file:
            items = pickle.load(db_file)
        return items
    else:
        return {}



def get_new_updates(db_name='dbfile'):
    logger.info("Looking For new Offers...")
    new_items = namshi_scraper()
    db = load_db(db_file_name=db_name)
    updates = set(new_items)-set(db)
    if len(updates) > 0:
        #print("There is new items that you should see.")
        updates = {k:new_items.get(k) for k in set(new_items)-set(db)}
        export_to_file(updates,db_name=db_name)
        for item in updates:
            logger.info(f"offer for {updates.get(item).name} found.")
    else:
        logger.info("there is no new offer.")
    return updates

if __name__=="__main__":
    get_new_updates(db_name='namshi')