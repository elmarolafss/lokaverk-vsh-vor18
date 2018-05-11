import requests
import json
from progress.bar import Bar

# https://ultimate-dot-acp-magento.appspot.com/categories_navigation?q=&UUID=8fb37bd6-aef1-4d7c-be3f-88bafef01308&page_num=1&category_id=180828100

how_many_pages = 5

category_ids = {
    "dresses": 180828100,
    "jackets": 180828228,
    "tops": 181230148,
    "jeans": 179381124,
    "pants": 181231428
}

all_links = {cat: [] for cat in category_ids}

new_links = input("\nGet new links? (y/n): ")

if new_links == "y":
    for cat in category_ids:
        for p_num in range(1,how_many_pages+1):
            url = f"https://ultimate-dot-acp-magento.appspot.com/categories_navigation?q=&UUID=8fb37bd6-aef1-4d7c-be3f-88bafef01308&category_id={category_ids[cat]}&page_num={p_num}"
            resp = requests.get(url=url)
            data = resp.json()
            for item in data["items"]:
                link_name = item["u"].split("/")[-1]
                if not link_name in all_links[cat]:
                    all_links[cat].append(link_name)
                    if "alt" in item:
                        if item["alt"]:
                            for alt_link in item["alt"]:
                                alt_link_name = alt_link[-1].split("/")[-1]
                                if not alt_link_name in all_links[cat]:
                                    all_links[cat].append(alt_link[-1].split("/")[-1])
        # print(all_links[cat])
        print(f"all_links{cat} has :", len(all_links[cat]), "product names")
    try:
        with open("clothes_links.json", "w+") as f:
            json.dump(all_links, f, indent=4)
            print("dumped info into clothes_links.json")
    except:
        print("something went wrong with writing to clothes_links.json...")
        raise

try:
    with open("clothes_links.json", "r") as f:
        all_links = json.load(f)
except:
    print("something went wrong with opening clothes_links.json...")
    raise

# print(all_links)

use_new_links = input("\nGet data from new links? (y/n): ")
if use_new_links == "y":
    all_clothes = {cat: {} for cat in category_ids}
    try:
        with open("all_products.json", "r") as f:
            all_clothes = json.load(f)
    except:
        all_clothes = {cat: {} for cat in category_ids}
        print("something went wrong with reading all_products.json...")

    for cat in category_ids:
        no_skip_cat = input(f"get data from {cat} category? (y/n): ")
        if no_skip_cat == "y":
            bar = Bar(f"Parsing data for {cat}", fill=u"\u2588", max=len(all_links[cat]), suffix="%(percent)d%%")

            clear_existing = input(f"Clear all existing clothes from {cat}? (y/n): ")

            all_clothes[cat] = {} if clear_existing == "y" else all_clothes[cat]

            for lname in all_links[cat]:
                skipitty = False
                url = f"https://www.fashionnova.com/products/{lname}.json"
                resp = requests.get(url=url)
                try:
                    data = resp.json()
                except:
                    print(f"Error with item {lname}... skipping")
                    skipitty = True
                if not skipitty:
                    prod = data["product"]

                    if not prod["handle"] in all_clothes[cat]:
                        all_clothes[cat][prod["handle"]] = {
                            "id": prod["handle"],
                            "title": prod["title"],
                            "color": prod["title"].split(" ")[-1],
                            "type": prod["product_type"],
                            "sizes": prod["options"][0]["values"],
                            "images": [img["src"] for img in prod["images"]],
                            "price": prod["variants"][0]["price"]
                        }
                bar.next()
            bar.finish()
    try:
        with open("all_products.json", "w+") as f:
            json.dump(all_clothes, f, indent=4)
            print("dumped info into all_products.json")
    except:
        print("something went wrong with writing to all_products.json...")
        raise
