import requests
from pushbullet import Pushbullet
import json

def check_stock(sku):
    r = requests.get("https://uk.webuy.com/product.php?sku={}".format(sku))
    if "buy this item" in r.text:
        return True
    else:
        return False

with open("config.json") as json_cfg:
    json_cfg = json.load(json_cfg)
    pb_key = json_cfg['pb_api_key']
    cex_item_list = json_cfg['item_list']
    cex_item_list = cex_item_list.split(';')
    cex_stock_list = json_cfg['item_current']
    cex_stock_list = cex_stock_list.split(";")
pb = Pushbullet(pb_key)

j = 0
json_cfg['item_current'] = ""

for i in cex_item_list:
    if (check_stock(i)):
        url = "https://uk.webuy.com/product.php?sku={}".format(i)
        if cex_stock_list[j] == "no":
            pb.push_note("CEX Stock Alert", "Item Detected In Stock {} \n You will be notified again when the item is out of stock.".format(url))
            json_cfg['item_current'] = json_cfg['item_current'] + "yes;"
        elif cex_stock_list[j] == "yes":
            pass
        else:
            print("HOW???")
            pass
    else:
        pass
    j += 1


with open ('config.json', 'w') as json_out:
    json.dump(json_cfg, json_out)
