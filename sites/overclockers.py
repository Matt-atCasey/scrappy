from curl_cffi import requests
import logging
from bs4 import BeautifulSoup
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_overclockers():
    urls = [
        "https://www.overclockers.co.uk/pc-components?pim_gpu_family_series%5B0%5D=RTX+50+Series"
    ]
    # ? urls = [
    # ?     "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-4060"
    # ? ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.overclockers.co.uk/pc-components/graphics-cards/nvidia-graphics-cards",
    }
    products = []
    logger.info("Fetching data from Overclockers...")

    # Create a session for persistent connections
    session = requests.Session()
    session.headers.update(headers)

    # Perform the requests using the session
    for url in urls:
        try:
            response = session.get(url, impersonate="chrome")
            if response.status_code == 200:
                logger.info(f"Data fetched successfully from {url}")
                products.extend(parse_overclockers(response.text))
            else:
                logger.error(
                    f"Failed to fetch data from {url}. Status Code: {response.status_code}"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to fetch data. {e}")
            return None
    return products


def parse_overclockers(response):
    products = []
    soup = BeautifulSoup(response, "lxml")
    main = (
        soup.find("main")
        .find("div", class_="main-container")
        .find("div", class_="mb-4")
        .find("div", class_="row")
        .find("div", class_="col-lg-9")
        .find("div", class_="row--listing-wrapper")
        .find("div", class_="row")
    )

    fail_count = 0
    for product in main.find_all("div", class_="col"):
        try:
            name_tag = product.select_one("[data-qa='ck-product-box--title-link']")
            name = name_tag.text.strip() if name_tag else None

            # Extract Price
            price_tag = product.select_one("[data-qa='price-current']")
            if price_tag:
                price_match = re.search(r"£([\d,]+\.?\d*)", price_tag.text)
                price = (
                    float(price_match.group(1).replace(",", ""))
                    if price_match
                    else None
                )
            else:
                price = None

            # If no name or price, skip this product and increment fail count
            if not name or price is None:
                fail_count += 1
                continue

            # Extract Link
            link_tag = product.select_one("[data-qa='ck-product-box--title-link']")
            link = (
                f"https://www.overclockers.co.uk{link_tag['href']}"
                if link_tag
                else "N/A"
            )

            # Extract Brand (assuming brand is part of the name)
            brand = "Asus" if "Asus" in name else None
            if "GeForce" in name:
                brand = name.split("GeForce")[0].strip().split()[-1]
            else:
                brand = None

            # Extract Stock Status
            stock_status = product.select_one(
                "[data-qa='availability_status_out_of_stock']"
            )
            in_stock = (
                stock_status is None
            )  # If 'Out of stock' tag is found, it's False

            products.append(
                {
                    "name": name,
                    "price": price,
                    "link": link,
                    "brand": brand,
                    "in_stock": in_stock,
                    "site": "Overclockers",
                }
            )

        except Exception as e:
            fail_count += 1
            continue

    logger.error(f"Failed to parse {fail_count} products")
    return products
