import logging
from bs4 import BeautifulSoup
import httpx


def scrape_scan():
    scan_urls = [
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5070-graphics-cards",
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5080-graphics-cards",
        "https://www.scan.co.uk/shop/computer-hardware/gpu-nvidia-gaming/geforce-rtx-5090-graphics-cards",
    ]

    all_products = []

    for url in scan_urls:
        try:
            page = httpx.get(
                url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                },
            )
            page.raise_for_status()  # Raise an HTTPError for bad responses
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logging.error(f"URL not found (404): {url}")
            elif e.response.status_code == 403:
                logging.warning(f"Access forbidden (403): {url}")
            else:
                logging.error(
                    f"HTTP error occurred for {url}: {e.response.status_code}"
                )
            continue
        except httpx.RequestError as e:
            logging.error(f"Network error occurred: {e}")
            continue

        soup = BeautifulSoup(page.content, "html.parser")

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
                    "price": product_price.strip(),
                    "link": product_link.strip(),
                    "in_stock": in_stock,
                    "site": "Scan",
                }
            )

        all_products.extend(new_products)

    return all_products
