from curl_cffi import requests
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_nvidia():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": "https://www.nvidia.com/",
    }

    urls = [
        "https://api.nvidia.partners/edge/product/search?page=1&limit=999&locale=en-gb&gpu=RTX%205060,RTX%205060%20Ti,RTX%205070,RTX%205070%20SUPER,RTX%205070%20Ti,RTX%205070%20Ti%20SUPER,RTX%205080,RTX%205080%20SUPER,RTX%205090&gpu_filter=RTX%205090~16,RTX%205080%20SUPER~16,RTX%205080~3,RTX%205070%20Ti%20SUPER~21,RTX%205070%20Ti~23,RTX%205070%20SUPER~21,RTX%205070~20,RTX%205060%20Ti~27,RTX%205060~21&category=GPU"
    ]
    logger.info("Fetching data from NVIDIA API...")
    # Perform the API request
    for url in urls:
        response = requests.get(url, headers=headers, impersonate="chrome")
        # Check the response
        if response.status_code == 200:
            try:
                response_json = response.json()
                return parse_nvidia_api_response(response_json)
            except Exception as e:
                logger.error(f"Failed! Products not yet available... {e}")
                logger.debug(response.text)
                return None
        else:
            logger.error(f"Failed to fetch data. Status Code: {response.status_code}")
            return None


def parse_nvidia_api_response(response):
    # Extract the products from the JSON response
    logger.info("Parsing NVIDIA API response...")
    new_products = []
    if not response:
        return new_products
    try:
        products = response.get("searchedProducts", {}).get("productDetails", [])
        for product in products:
            product_name = product.get("productTitle")
            product_price = product.get("productPrice")
            product_manufacturer = product.get("manufacturer")
            product_link = product.get("internalLink")
            in_stock = product.get("productAvailable")
            new_products.append(
                {
                    "name": product_name.strip() if product_name else "Unknown",
                    "brand": (
                        product_manufacturer.strip()
                        if product_manufacturer
                        else "Unknown"
                    ),
                    "price": product_price.strip() if product_price else "Unknown",
                    "link": product_link.strip() if product_link else "",
                    "in_stock": in_stock,
                    "site": "NVIDIA",
                }
            )
            logger.debug(f"Found product: {product_name}")
    except Exception as e:
        logger.error(f"Failed to parse response: {e}")
        logger.debug(response)
        return []
    return new_products
