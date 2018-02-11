import requests
from pushbullet import Pushbullet
import json
import re


def check_stock(sku,stock):
    r = requests.get("https://uk.webuy.com/product.php?sku={}".format(sku))
    rt = r.text
    if "buy this item" in rt and stock == "no":
        #print("In stock, new known")
        return "isNK"
    elif "buy this item" in rt and stock == "yes":
        #print("In stock, pre known")
        return "isPK"
    elif "buy this item" not in rt and stock == "yes":
        #print("Was in stock, now out, new known")
        return "wisNoNK"
    elif "buy this item" not in rt and stock == "no":
        #print("Not in stock, pre known")
        return "nisPK"

with open("config.json") as json_cfg:
    json_cfg = json.load(json_cfg)
    pb_key = json_cfg['pb_api_key']
    items = json_cfg['items']['skus']
    stocks = json_cfg['items']['stocks']

pb = Pushbullet(pb_key)

stocked = []
notStocked = []

for i in items:
    stock = stocks[items.index(i)]
    result = check_stock(i, stock)
    reS = "(?<=\<title\>)(.*)(?= - CeX \(UK\): - Buy, Sell, Donate\<\/title\>)"
    itemName = requests.get("https://uk.webuy.com/product.php?sku={}".format(i))
    itemName = itemName.text
    try:
        itemName = re.search(reS, itemName).group(0)
    except:
        itemName = "Couldn't Parse Name"
    if result == "isNK":
        #In stock, new known
        #print("{} is now in stock".format(i))
        pb.push_note("CEX Stock Alert", "Item \"{}\" Detected In Stock https://uk.webuy.com/product.php?sku={}".format(itemName, i))
        stocked.append(i)
    elif result == "isPK":
        #In stock, pre known
        pass
    elif result == "wisNoNK":
        #Was in stock, now out, new known
        #print("{} is now out of stock".format(i))
        pb.push_note("CEX Stock Alert", "Item \"{}\" Detected Out Of Stock https://uk.webuy.com/product.php?sku={}".format(itemName, i))
        notStocked.append(i)
    elif result == "nisPK":
        #Not in stock, pre known
        pass

#Make the json to re-write :)

itemsJson = {"skus":[],"stocks":[]}

for i in items:
    itemsJson['skus'].append(i)
    if i in stocked:
        #Item is now stocked
        itemsJson['stocks'].append("yes")
    elif i not in stocked and i in notStocked:
        #Item is not stocked
        itemsJson['stocks'].append("no")
    else:
        oldState = stocks[items.index(i)]
        itemsJson['stocks'].append(oldState)            

#print(itemsJson)

#Lets Write
with open('config.json', 'r+') as json_cfg:
    json_cfgW = json.load(json_cfg)
    json_cfgW['items'] = itemsJson
    json_cfg.seek(0)
    json.dump(json_cfgW, json_cfg, indent=4)
    json_cfg.truncate()