import httpx
from bs4 import BeautifulSoup
from classes import Product
import json
from rich import print as rprint


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


# ** Pls return scrapes with a dictionary and then create a Product object from the dictionary in main.py :)
def scrape_scan():
    scan_urls = [
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5070-graphics-cards",
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5080-graphics-cards",
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5090-graphics-cards",
    ]

    all_products = []

    for url in scan_urls:
        try:
            page = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"})
            page.raise_for_status()  # Raise an HTTPError for bad responses
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                rprint(f"[red]URL not found (404): {url}[/red]")
            elif e.response.status_code == 403:
                rprint(f"[orange]Access forbidden (403): {url}[/orange]")
            else:
                rprint(
                    f"[red]HTTP error occurred for {url}: {e.response.status_code}[/red]"
                )
            continue
        except httpx.RequestError as e:
            rprint(f"[red]Network error occurred: {e}[/red]")
            continue

        soup = BeautifulSoup(page.content, "html.parser")

        # Find the product group list
        product_group = soup.find("ul", class_="product-group")
        if not product_group:
            rprint(f"[yellow]No products found on page: {url}[/yellow]")
            continue

        products = product_group.find_all("li")
        new_products = []

        for product in products:
            product_name = product.get("data-description")
            product_manufacturer = product.get("data-manufacturer")
            product_price = product.get("data-price") or "0"

            # Handle special price cases
            if product_price == "999999.00" or product_price == "0":
                product_price = "Out of stock"

            product_link = "https://www.scan.co.uk/" + product.find("a")["href"]

            # Append as dictionary
            new_products.append(
                {
                    "name": product_name.strip() if product_name else "Unknown",
                    "brand": (
                        product_manufacturer.strip()
                        if product_manufacturer
                        else "Unknown"
                    ),
                    "price": product_price.strip(),
                    "link": product_link.strip(),
                }
            )

        all_products.extend(new_products)

    return all_products


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
