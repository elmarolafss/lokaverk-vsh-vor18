import requests
from bs4 import BeautifulSoup
import unicodedata
import re


class ProductItem:
    def __init__(self, name, price, type, colors, images, info, sizes):
        self.name = name
        self.price = price
        self.type = type
        self.colors = colors
        self.images = images
        self.info = info
        self.sizes = sizes

all_products = []

all_links = {
    "dresses": [],
    # "jackets": [],
    # "tops-1": [],
    # "jeans": [],
    # "shoes": [],
}

how_many_pages = 1

# safnar nöfnum á fötum í öllum flokkum
for category in all_links:
        for page_num in range(1, how_many_pages + 1):
            page_address = f"https://www.fashionnova.com/collections/{category}?page={page_num}"
            print(f"now visiting : {page_address}")
            page = requests.get(page_address)
            soup = BeautifulSoup(page.content, "html.parser")
            item_divs = soup.find_all("div", class_="product-item")
            for item_div in item_divs:
                item_name = item_div.find_all("a")[0]["href"].split("/")[-1]
                all_links[category].append(item_name)
                print(f"just added: {item_name} to all_links {category} list")
        print(f"WOW! i just added {len(all_links[category])} item names to the list!")


def map_to_right_category_name(string):
    map_names = {
        "dresses": "Dress",
        "jackets": "Jacket",
        "tops-1": "Top",
        "jeans": "Jeans",
        "shoes": "Shoe"
    }
    return map_names[string] if string in map_names else string

def sanitize_string(string):
    almost_cleaned = unicodedata.normalize("NFKD", string).strip()
    cleaned = almost_cleaned.replace("\"", "").replace("\\", "")
    return re.sub(r'(%)(?!\s)', "% ", cleaned)  # regex er frábært

how_many_items = 10
counter = 0

# heimsæækir fötin og setur inn upplýsingarnar í ProdutItem clasa
for category in all_links:
    for item_page_name in all_links[category]:
        counter += 1
        product_other_colors_raw = []
        page_address = f"https://www.fashionnova.com/collections/{category}/products/{item_page_name}"
        page = requests.get(page_address)
        soup = BeautifulSoup(page.content, "html.parser")
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
