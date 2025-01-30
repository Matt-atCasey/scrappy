from curl_cffi import requests
import logging
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_ebuyer():
    urls = [
        "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-5070-Ti",
        "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-5080",
        "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-5090",
    ]
    # ? urls = [
    # ?     "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia/subcat/GeForce-RTX-4060"
    # ? ]
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.ebuyer.com/store/Components/cat/Graphics-Cards-Nvidia",
    }
    products = []
    logger.info("Fetching data from Ebuyer...")

    # Create a session for persistent connections
    session = requests.Session()
    session.headers.update(headers)

    # Perform the requests using the session
    for url in urls:
        try:
            response = session.get(url, impersonate="chrome")
            if response.status_code == 200:
                logger.info(f"Data fetched successfully from {url}")
                products.extend(parse_ebuyer(response.text))
            else:
                logger.error(
                    f"Failed to fetch data from {url}. Status Code: {response.status_code}"
                )
                return None
        except Exception as e:
            logger.error(f"Failed to fetch data. {e}")
            return None
    return products


def parse_ebuyer(response):
    products = []
    soup = BeautifulSoup(response, "html.parser")
    main = (
        soup.find("section", class_="main-content")
        .find("div", class_="wrapper")
        .find("div", class_="holder")
        .find("div", class_="listing")
        .find("div", id="list-view")
    )
    for product in main.find_all("div", class_="listing-product"):
        item_name = product.get("data-cnstrc-item-name")
        brand = (
            item_name.split("NVIDIA")[0].strip() if "NVIDIA" in item_name else "Unknown"
        )
        price = product.get("data-cnstrc-item-price")
        link = "https://www.ebuyer.com" + product.find(
            "div", class_="listing-image"
        ).find("a").get("href")
        in_stock = (
            True
            if product.find("div", class_="listing-price").find(
                "div", class_="promo-message promo-message--delivery"
            )
            else False
        )
        site = "Ebuyer"
        products.append(
            {
                "name": item_name,
                "brand": brand,
                "price": price,
                "link": link,
                "in_stock": in_stock,
                "site": site,
            }
        )

    return products
