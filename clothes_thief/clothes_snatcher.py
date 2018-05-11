from bs4 import BeautifulSoup
import unicodedata
import requests
import json
import re
import sys

class ProductItem:
    def __init__(self, lname, name, price, ctype, colors, images, info, sizes):
        self.link_name = lname
        self.name = name
        self.price = price
        self.type = ctype
        self.colors = colors
        self.images = images
        self.info = info
        self.sizes = sizes

    def __repr__(self):
        return f"{self.name} of type {self.type}"

    def __str__(self):
        return self.link_name

    def sql_safe_dict(self):
        _d = {
            "lname": self.link_name,
            "name": self.name,
            "price": self.price,
            "discount": 0,
            "category": self.type,
            "color": self.colors[0],
            "colors": flat_arr(self.colors),
            "imgs": flat_arr(self.images),
            "info": flat_arr(self.info),
            "sizes": flat_arr(self.sizes)
        }
        return _d

def flat_arr(arr, sep="$"):
    # flatten array with separator e.g [1,2] -> 1$2
    return sep.join(str(_) for _ in arr)

def map_to_right_category_name(string):
    map_names = {
        "dresses": "Dress",
        "jackets": "Jacket",
        "tops-1": "Top",
        "jeans": "Jeans",
        "pants": "Pants"
    }
    return map_names[string] if string in map_names else string

def sanitize_string(string):
    almost_cleaned = unicodedata.normalize("NFKD", string).strip()
    cleaned = almost_cleaned.replace("\"", "").replace("\\", "")
    return re.sub(r'(%)(?!\s)', "% ", cleaned)  # regex er frábært

all_products = []
all_links = {
    "dresses": [],
    "jackets": [],
    "tops-1": [],
    "jeans": [],
    "pants": [],
}
how_many_pages = 5
picker = 0

while picker not in ["1","2"]:
    picker = input("1. Get item links\n2. Pick data from item links\nSelect 1 or 2: ")

if picker == "1":
    # safnar nöfnum á fötum í öllum flokkum
    for category in all_links:
            for page_num in range(1, how_many_pages + 1):
                page_address = f"https://www.fashionnova.com/collections/{category}?page={page_num}"
                print(f"now visiting : {page_address}")
                page = requests.get(page_address)
                soup = BeautifulSoup(page.content, "html.parser")
                print(soup)
                item_lis = soup.find_all("li", class_="isp_product_info")
                print(item_lis)
                for item_li in item_lis:
                    item_name = item_li.find_all("a")[0]["href"].split("/")[-1]
                    print(item_name)
                    all_links[category].append(item_name)
                    print(f"just added: {item_name} to all_links {category} list")
            print(f"WOW! i just added {len(all_links[category])} item names to the list!")
    try:
        with open("clothes_links.json", "w+") as f:
            json.dump(all_links, f)
        print("dumped info into clothes_links.json")
    except:
        print("something went wrong with clothes_links.json...")
        raise
elif picker == "2":
    try:
        with open("clothes_links.json", "r") as f:
            all_links = json.load(f)
    except:
        print("something went wrong with clothes_links.json...")
        raise
    # heimsækir fötin og setur inn upplýsingarnar í ProdutItem klasa
    for category in all_links:
        for item_page_name in all_links[category]:
            try:
                product_other_colors_raw = []
                page_address = f"https://www.fashionnova.com/collections/{category}/products/{item_page_name}"
                page = requests.get(page_address)
                soup = BeautifulSoup(page.content, "lxml")
                product_info_section = soup.select("#product-info")[0]
                # byrja plokka gögn hér úr product info section
                product_name = product_info_section.h1.string
                product_price = float(product_info_section.select(".price")[0]
                                      .select("meta")[1]["content"])
                product_type = map_to_right_category_name(category)
                product_colors = [str(item_page_name.split("-")[-1])]
                product_other_colors_raw = soup.find_all("a", class_="link-color-swatch")
                if product_other_colors_raw:
                    for other_color_a_tag in product_other_colors_raw:
                        all_links[category].append(str(other_color_a_tag["href"].split("/")[-1]))
                        other_color = str(other_color_a_tag.get("href").split("-")[-1])
                        if other_color not in product_colors:
                            product_colors.append(other_color)
                product_script_tag = soup.find_all("script")[-6].get_text()
                product_image_links_raw = re.findall(r'(?<=\[)\".+?\"(?=\])', product_script_tag)[-2]
                product_image_links_raw = product_image_links_raw.split(",")
                product_image_links = list(map(sanitize_string, product_image_links_raw))
                product_info_raw = soup.find_all("div", class_="group-body")[0].ul.contents[1:-1:2]
                product_info = [sanitize_string(info_line.get_text()) for info_line in product_info_raw]

                product_sizes_raw = re.findall(r'(?<=\[)\".+?\"(?=\])', product_script_tag)
                product_sizes_raw = list(filter(lambda x: len(x) < 5, product_sizes_raw))
                product_sizes = list(map(sanitize_string, product_sizes_raw))
                product = ProductItem(item_page_name, product_name, product_price, product_type, product_colors, product_image_links, product_info, product_sizes)
                all_products.append(product)
                print(f"just added {product} to all_products")
                # print(product.sql_safe_dict())
            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                print(f"Unexpected error:{sys.exc_info()[0]}")
        print(f"just finished adding all {category} to all_products")
    print(f"all products = {all_products}")

