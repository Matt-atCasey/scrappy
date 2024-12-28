import json
import time
from classes import Product
from rich.progress import track
from sites import scrape_scan, scrape_nvidia
from discord_bot import DiscordNotifier
from dotenv import load_dotenv
import asyncio
import os


def scrape_all():
    # where all scrapers will go
    scan_products = scrape_scan()
    nvidia_products = scrape_nvidia()

    return scan_products + nvidia_products


async def check_for_changes(new_products):
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
        # Convert dictionary items to Product objects
        for product in new_products:
            if product not in existing_products:
                print(
                    f"\n\033[92m[NEW]\033[0m {product['name']}\n\tPrice: £{product['price']}\n\tLink: {product['link']}"
                )
                await notifier.send_notification(
                    f"**[NEW]** {product['name']}\nPrice: £{product['price']}\nLink: {product['link']}"
                )

        # Find products that were removed
        for product in existing_products:
            if product not in new_products:
                print(
                    f"\n\033[91m[REMOVED]\033[0m {product['name']}\n\tPrice: £{product['price']}\n\tLink: {product['link']}"
                )
                await notifier.send_notification(
                    f"**[REMOVED]** {product['name']}\nPrice: £{product['price']}\nLink: {product['link']}"
                )
        # write new products to products.json
        with open("products.json", "w") as f:
            json.dump(new_products, f, indent=4)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")

    notifier = DiscordNotifier(token, channel_id)

    async def main():
        while True:
            new_products = scrape_all()
            await check_for_changes(new_products)
            for _ in track(range(30), description="Sleeping for 30 seconds..."):
                time.sleep(1)

    asyncio.run(notifier.run_with_task(main))
