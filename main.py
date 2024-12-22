import json
import time
import httpx  # type: ignore
from bs4 import BeautifulSoup
from classes import Product
from rich.progress import track


def scrape_scan():
    url = "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/geforce-rtx-4090-graphics-cards"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    page = httpx.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    new_products = []

    # # grab every list element in the ul "product-group"
    products = soup.find("ul", class_="product-group").find_all("li")
    for product in products:
        product_name = product.find("div").find("span", class_="description").text
        product_price = (
            product.find("div", class_="priceAvailability")
            .find("div", class_="priceWishlistBuy")
            .find("div", class_="leftColumn")
            .find("span", class_="price")
            .text.strip()
        )
        product_link = product.find("a")["href"]
        # get rid of parse weirdness
        product_price = "".join(
            part.strip() for part in product_price if part.strip()
        ).replace("£", "")

        # create a new product object
        new_product = Product(product_name, product_price, product_link)
        # add the new product to the list as json object
        new_products.append(new_product.__dict__)
        print(new_product)
    return new_products


def scrape_all():

    # where all scrapers will go
    return scrape_scan()


def check_for_changes(new_products):
    # check if the new products are in the existing products
    # if not, add them and notify changes
    # load products.json if it exists
    try:
        with open("products.json", "r") as f:
            existing_products = json.load(f)
    except FileNotFoundError:
        existing_products = []

    if new_products != existing_products:
        print("Changes detected!")
        # Find products that were added or modified
        for product in new_products:
            if product not in existing_products:
                print(
                    f"\n[NEW/MODIFIED] {product['name']}\n\tPrice: £{product['price']}"
                )

        # Find products that were removed
        for product in existing_products:
            if product not in new_products:
                print(f"\n[REMOVED] {product['name']}\n\tPrice: £{product['price']}")
        # write new products to products.json
        with open("products.json", "w") as f:
            json.dump(new_products, f, indent=4)


def main():
    new_products = scrape_all()
    check_for_changes(new_products)
    for i in track(range(60), description="Sleeping for 60 seconds..."):
        time.sleep(1)


if __name__ == "__main__":
    while True:
        main()
