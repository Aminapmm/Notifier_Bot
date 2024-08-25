from bs4 import BeautifulSoup as bs
from requests import request
from datetime import datetime
import pickle
from urllib.parse import urljoin
import os
import time
import logging
logger = logging.getLogger(__name__)

class Item:
    def __init__(self,element):
        self.link = urljoin("https://namshi.com",element['href'])
        self.serial = element['href'].split("/")[3]
        self.timer = element.find(class_="TimerSale_timer__321ZF")
        self.image = element.find('img')['src']
        get_price = lambda price:price[1].text +" "+price[0].text
        self.price = get_price(element.select((".ProductPrice_value__hnFSS,.ProductPrice_currency__issmK")))
        get_name = lambda name:name[0].text+"-"+name[1].text
        self.name = get_name(element.select(".ProductBox_brand__oDc9f,.ProductBox_productTitle__6tQ3b"))
        self.date_updated = time.time()
    
    def __str__(self):
        return f"{self.name}\n{self.price}"
    
    def __eq__(self,other):
        return self.price == other.price

    def __ne__(self, other: object) -> bool:
        return self.price != other.price
    
def namshi_scraper(url="https://www.namshi.com/uae-en/men-shoes-sports-trainers/?page=1&f%5Bbrand_code%5D=nike&f%5Bbrand_code%5D=under_armour&sort%5Bby%5D=discount_percent&sort%5Bdir%5D=desc"):
    logging.basicConfig(filename="log.txt",level=logging.INFO)
    res = request("GET",url).content
    soup = bs(res,'lxml')
    items = soup.select(".ProductBox_container__wiajf .ProductBox_productBox__tPpGm")
    return items

def export_to_file(items:dict,db_name='dbfile'):
    #file_name = datetime.now().strftime("%d%b%y")
    with open(f"db/{db_name}",'ab') as db_file:
        pickle.dump(items,db_file)

def load_db(db_file_name="dbfile"):#load db_file
    with open(f"db/{db_file_name}",'rb') as db_file:
        items = pickle.load(db_file)
    return items



def get_new_updates(db_name='dbfile'):
    new_items = {obj.serial: obj for obj in map(lambda x:Item(x),namshi_scraper())}
    db = load_db(db_name)
    updates = set(new_items)-set(db)
    if len(updates) > 0:
        print("There is new items that you should see.")
        updates = {k:new_items.get(k) for k in set(new_items)-set(db)}
        export_to_file(updates,db_name=db_name)
    return updates

    