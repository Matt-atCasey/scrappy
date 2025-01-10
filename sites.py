import httpx
from bs4 import BeautifulSoup
from classes import Product
import json


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# ** Pls return scrapes with a dictionary and then create a Product object from the dictionary in main.py :)


def scrape_scan():
    url = "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/geforce-rtx-5080-graphics-cards"
    page = httpx.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    new_products = []

    # Grab every list element in the ul "product-group"
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

        # Return as a dictionary
        new_products.append(
            {
                "name": product_name,
                "brand": product_manufacturer,
                "price": product_price,
                "link": product_link,
            }
        )

    return new_products


# NOT WORKING :(
def scrape_nvidia():

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
    return new_products
