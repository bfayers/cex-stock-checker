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


pb = Pushbullet(pb_key)

for i in cex_item_list:
    if (check_stock(i)):
        url = "https://uk.webuy.com/product.php?sku={}".format(i)
        pb.push_note("CEX Stock Alert", "Item Detected In Stock {}".format(url))
    else:
        pass
