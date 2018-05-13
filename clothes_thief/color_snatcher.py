from bs4 import BeautifulSoup
import requests
import json
import re
import sys

c_to_hex = {
    "black": "#000000",
    "white": "#ffffff",
    "yellow": "#fffe4e",
    "rust": "#f4ac94",
    "mauve": "#eda3c4",
    "brown": "#8b4513",
    "red": "#ee1212",
    "grey": "#bebcbd",
    "royal": "#0000cd",
    "multi": "linear-gradient(to right, orange , yellow, green, cyan, blue, violet)",
    "navy": "#182373",
    "burgundy": "#870f11",
    "sage": "#768f7c",
    "jade": "#56dfc1",
    "mustard": "#dac90a",
    "pink": "#f4ac94",
    "cream": "#f7eee5",
    "blush": "#f8d3e4",
    "green": "008000",
    "orange": "ff8c00",
    "tomato": "#f44336",
    "marsala": "#eda3c4",
    "purple": "#9400d3"
} # þetta er hér ef eitthvað klikkar

def fix_upper_hex(_d):
    for _k in _d:
        if list(filter(lambda x: x.isupper(), _d[_k])): # elska python
            _d[_k] = _d[_k].lower()
    return _d

def exit_write():
    try:
        with open("colors.json", "w+") as f:
            json.dump(c_to_hex, f, indent=4)
        print("dumped info into colors.json")
    except:
        print("something went wrong with colors.json...")
        raise

try:
    with open("colors.json", "r") as f:
        c_to_hex = json.load(f)
        c_to_hex = fix_upper_hex(c_to_hex)
except:
    print("something went wrong with colors.json...")
    raise

try:
    with open("clothes_links.json", "r") as f:
        all_links = json.load(f)
except:
    print("something went wrong with clothes_links.json...")
    raise

sel = input("get colors / find unnamed / fix colors.json / use new all_products.json = 1/2/3/4: ")

if sel == "1":
    for category in all_links:
        skip_cat = input(f"skip category {category}? y/n: ")
        if skip_cat != "y":
            for item_page_name in all_links[category]:
                try:
                    product_other_colors_raw = []
                    page_address = f"https://www.fashionnova.com/collections/{category}/products/{item_page_name}"
                    page = requests.get(page_address)
                    soup = BeautifulSoup(page.content, "lxml")
                    if "unavailable" in soup.title.string:
                        exit_write()
                        print("god damn it")
                        raise
                    product_colors = [str(item_page_name.split("-")[-1])]
                    product_other_colors_raw = soup.find_all("a", class_="link-color-swatch")
                    if product_other_colors_raw:
                        for other_color_a_tag in product_other_colors_raw:
                            all_links[category].append(str(other_color_a_tag["href"].split("/")[-1]))
                            other_color_name = other_color_a_tag["href"].split("/")[-1].split("-")[-1]
                            if not other_color_name in c_to_hex:
                                c_to_hex[other_color_name] = other_color_a_tag.div["style"].split(" ")[-1]
                                other_color = str(other_color_a_tag.get("href").split("-")[-1])
                                if other_color not in product_colors:
                                    product_colors.append(other_color)
                    if len(product_colors) > 1:
                        print(f"i just found these colors {product_colors[1:]}")
                        print("the new c_to_hex is\n\n", c_to_hex)
                except (KeyboardInterrupt, SystemExit):
                    print(c_to_hex)
                    exit_write()
                    raise
                except:
                    print(c_to_hex)
                    print(f"Unexpected error:{sys.exc_info()[0]}")
    exit_write()
elif sel == "2":
    try:
        for category in all_links:
            skip_cat = input(f"skip category {category}? y/n: ")
            if skip_cat != "y":
                for item_page_name in all_links[category]:
                    color = item_page_name.split("-")[-1]
                    if not color in c_to_hex:
                        print(f"i dont know {color}")
                        new_val = input("tell me: ")
                        c_to_hex[color] = new_val
    except:
        exit_write()
elif sel == "3":
    exit_write()
elif sel == "4":
    try:
        with open("all_products.json", "r") as f:
            all_prods = json.load(f)
    except:
        print("something went wrong with reading all_products.json...")
        raise

    for cat in all_prods:
        for prod in all_prods[cat]:
            if not prod['color'] in c_to_hex:
                print("unknown color", prod['color'], "what do i do?")
                ask_me = input(f"\nWhat hex color is {prod['color']}: ")
                c_to_hex[prod['color']] = ask_me
    exit_write()
