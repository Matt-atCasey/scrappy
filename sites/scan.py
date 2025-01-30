import logging
from bs4 import BeautifulSoup
from curl_cffi import requests


def scrape_scan():
    scan_urls = [
        "https://www.scan.co.uk/shop/gaming/gpu-nvidia-gaming/4041/4039/4036/4040",
    ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.scan.co.uk/",
    }
    all_products = []

    for url in scan_urls:
        try:
            response = requests.get(url, headers=headers, impersonate="chrome")
            response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.errors.RequestsError as e:
            if response.status_code == 404:
                logging.error(f"URL not found (404): {url}")
            elif response.status_code == 403:
                logging.warning(f"Access forbidden (403): {url}")
            else:
                logging.error(f"HTTP error occurred for {url}: {response.status_code}")
            continue
        except Exception as e:
            logging.error(f"Network error occurred: {e}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")

        # Find the product group list
        product_group = soup.find("ul", class_="product-group")
        if not product_group:
            logging.warning(f"No products found on page: {url}")
            continue

        products = product_group.find_all("li")
        new_products = []

        for product in products:
            product_name = product.get("data-description")
            product_manufacturer = product.get("data-manufacturer")
            product_price = product.get("data-price") or "0"

            # Handle special price cases
            if product_price == "999999.00" or product_price == "0":
                product_price = None
            product_link = "https://www.scan.co.uk/" + product.find("a")["href"]
            in_stock = True if product_price else False

            # Append as dictionary
            new_products.append(
                {
                    "name": product_name.strip() if product_name else "Unknown",
                    "brand": (
                        product_manufacturer.strip()
                        if product_manufacturer
                        else "Unknown"
                    ),
                    "price": product_price.strip() if product_price else "Unknown",
                    "link": product_link.strip(),
                    "in_stock": in_stock,
                    "site": "Scan",
                }
            )

        all_products.extend(new_products)

    return all_products
