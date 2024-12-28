import httpx
from bs4 import BeautifulSoup
import requests
from classes import Product
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


def scrape_scan():
    url = "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/geforce-rtx-4080-super-graphics-cards"
    page = httpx.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    new_products = []

    # # grab every list element in the ul "product-group"
    products = soup.find("ul", class_="product-group").find_all("li")
    for product in products:
        product_name = product.get("data-description")
        product_manufacturer = product.get("data-manufacturer")
        try:
            product_price = product.get("data-price")
            if product_price == "999999.00" or product_price == "0":
                product_price = "Out of stock"
        except AttributeError:
            product_price = "0"

        product_link = "https://www.scan.co.uk/" + product.find("a")["href"]

        # create a new product object
        new_product = Product(
            product_name, product_manufacturer, product_price, product_link
        )
        # add the new product to the list as json object
        new_products.append(new_product.__dict__)
        print(new_product)
    return new_products


def scrape_nvidia():
    # url = "https://api.nvidia.partners/edge/product/search?locale=en-gb&page=1&limit=12&gpu=RTX%204090&gpu_filter=RTX%204090&category=GPU"
    # cookies = "bm_sv=6AEC9321DD7DD295341B4CF471488C68~YAAQruQWAhQHltuTAQAAuiM3ChqrrXmiXOVd34s9HwARy/ZQtPUBVErn5027/32erXUoh0XiNZ4PbGp/LGkBCSIuHPTVs35FgpofXrB2tv3JuCncMOFdA03ZTvuBFZtsd5xHUn8w9O3PI+sxoNeixX+3xkz2HlLa7zcsAxyvRjcBFzn+UXdvVh+ZRiPJwFj6pdnvKstyxrYNEdQh72t8Nmx6FHjQ8Ir1OjzzdIFsAHQmq1ZaJkqInbSNBnrW/SE9~1"
    # headers = {
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    #     "Set-Cookie": cookies,
    # }
    # response = requests.get(url, headers=headers)
    # data = response.json()
    # print(data)

    # imported json file for testing
    with open("nvidia_test.json", "r") as f:
        data = json.load(f)

    new_products = []

    # loop through the json response and extract the product details into a new product object
    product_list = data["searchedProducts"]["productDetails"]
    for product in product_list:
        product_name = product["displayName"]
        product_manufacturer = product["manufacturer"]
        product_price = product["productPrice"]
        product_price = product_price.replace("Â", "")
        product_link = product["internalLink"]
        new_product = Product(
            product_name, product_manufacturer, product_price, product_link
        )
        new_products.append(new_product.__dict__)
        print(new_product)
    return new_products


scrape_nvidia()
