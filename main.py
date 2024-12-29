import json
import time
from classes import Product
from rich.progress import Progress, TaskID
from sites import scrape_scan, scrape_nvidia
from discord_bot import DiscordNotifier
from dotenv import load_dotenv
import asyncio
import os
import logging
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def scrape_all():
    scan_products = []
    nvidia_products = []

    try:
        scan_products = scrape_scan()
    except Exception as e:
        logger.error(f"Error scraping Scan: {e}")

    try:
        nvidia_products = scrape_nvidia()
    except Exception as e:
        logger.error(f"Error scraping Nvidia: {e}")

    # Combine and deduplicate products based on name
    all_products = scan_products + nvidia_products
    seen_names = set()
    unique_products = []

    for product in all_products:
        if product["name"] not in seen_names:
            seen_names.add(product["name"])
            unique_products.append(product)

    return unique_products


def check_for_changes(scraped_products):
    try:
        with open("products.json", "r") as f:
            existing_products = json.load(f)
    except FileNotFoundError:
        existing_products = []

    if scraped_products != existing_products:
        print("Changes detected!")
        # Convert dictionary items to Product objects
        scraped_products = [Product(**product) for product in scraped_products]
        existing_products = [Product(**product) for product in existing_products]

        # Find products that were added or modified
        added_products = [
            product for product in scraped_products if product not in existing_products
        ]
        modified_products = [
            product for product in scraped_products if product in existing_products
        ]

        # Save the new products to products.json
        with open("products.json", "w") as f:
            json.dump([product.__dict__ for product in scraped_products], f, indent=4)

        return added_products, modified_products

    # Return empty lists if no changes are detected
    return [], []


async def check_changes_and_notify():
    while True:
        scraped_products = scrape_all()
        added, modified = check_for_changes(scraped_products)

        # Send a single notification for all added products
        if added:
            try:
                added_message = "🆕 **New Products Added!**\n\n"
                # Sort products by name to ensure consistent order
                for product in sorted(added, key=lambda x: x.name):
                    added_message += f"📦 **{product.name}**\n💰 Price: £{product.price}\n🔗 Link: {product.link}\n\n"
                await notifier.send_notification(added_message)
                logger.info(f"Sent notification for {len(added)} new products")
            except Exception as e:
                logger.error(f"Failed to send added notification: {e}")

        # Send a single notification for all modified products
        if modified:
            try:
                modified_message = "🔄 **Products Modified!**\n\n"
                # Sort products by name to ensure consistent order
                for product in sorted(modified, key=lambda x: x.name):
                    modified_message += f"📦 **{product.name}**\n💰 Price: £{product.price}\n🔗 Link: {product.link}\n\n"
                await notifier.send_notification(modified_message)
                logger.info(f"Sent notification for {len(modified)} modified products")
            except Exception as e:
                logger.error(f"Failed to send modified notification: {e}")

        # Random delay between checks
        delay = random.randint(10, 20)
        logger.info(f"Waiting {delay} seconds before next check...")
        with Progress() as progress:
            task = progress.add_task("[cyan]Waiting for next check...", total=delay)
            for _ in range(delay):
                await asyncio.sleep(1)
                progress.advance(task, 1)


if __name__ == "__main__":
    load_dotenv()
    token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("DISCORD_CHANNEL_ID")

    if not token or not channel_id:
        raise ValueError("Missing DISCORD_TOKEN or DISCORD_CHANNEL_ID in .env file")

    notifier = DiscordNotifier(token, int(channel_id))
    notifier.run_with_task(check_changes_and_notify)
