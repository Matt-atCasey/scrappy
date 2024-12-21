import httpx
from bs4 import BeautifulSoup
from classes import Product


def scrape_scan():
    url = "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/geforce-rtx-4090-graphics-cards"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    page = httpx.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

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
        print(new_product)


scrape_scan()
