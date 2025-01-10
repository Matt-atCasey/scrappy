import json
from textwrap import shorten
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
    scraped_products = []

    # Define your scrapers here
    scrapers = [scrape_scan]

    for scraper in scrapers:
        try:
            results = scraper()
            scraped_products.extend(results)
            logger.info(f"Scraped {len(results)} products with {scraper.__name__}")

        except Exception as e:
            logger.error(f"Failed to scrape with {scraper.__name__}: {e}")

    # Save results to a JSON file
    try:
        with open("new_scrape.json", "w") as f:
            json.dump(scraped_products, f, indent=4)
        logger.info(f"Scraped products saved to new_scrape.json")
    except Exception as e:
        logger.error(f"Failed to save scraped products to JSON: {e}")

    return scraped_products


def check_for_changes(new_products):
    try:
        with open("products.json", "r") as f:
            try:
                existing_products = [Product(**p) for p in json.load(f)]
            except json.JSONDecodeError:
                existing_products = []
    except FileNotFoundError:
        existing_products = []

    new_products = [Product(**p) for p in new_products]
    logger.info(f"Loaded {len(existing_products)} existing products")

    # Detect added products
    added_products = [p for p in new_products if p not in existing_products]
    logger.info(f"Detected {len(added_products)} new products")

    # Detect modified products
    modified_products = []
    for new_product in new_products:
        for old_product in existing_products:
            if new_product.name == old_product.name:  # Match by name
                changes = new_product.compare(old_product)
                if changes:
                    modified_products.append((new_product, changes))

    # Detect deleted products
    deleted_products = [
        product for product in existing_products if product not in new_products
    ]

    # Save the updated list to products.json
    with open("products.json", "w") as f:
        json.dump([p.to_dict() for p in new_products], f, indent=4)

    return added_products, modified_products, deleted_products


async def check_changes_and_notify():
    """
    Periodically checks for changes in scraped products and sends notifications for added and modified products.
    """
    while True:
        scraped_products = scrape_all()
        added, modified, deleted = check_for_changes(scraped_products)

        # Discord message limit (including Markdown and emojis)
        DISCORD_MESSAGE_LIMIT = 2000

        # Send a single notification for all added products
        if added:
            try:
                added_message = "🆕 **New Products Added!**\n\n"
                for product in sorted(added, key=lambda x: x.name):
                    product_message = (
                        f"📦 **{product.name}**\n"
                        f"💰 Price: {product.price}\n"
                        f"🔗 [Product Link]({product.link})\n\n"
                    )
                    # Ensure message stays within Discord's limit
                    if (
                        len(added_message) + len(product_message)
                        > DISCORD_MESSAGE_LIMIT
                    ):
                        await notifier.send_notification(added_message)
                        added_message = ""  # Start a new message
                    added_message += product_message

                if added_message:
                    await notifier.send_notification(added_message)

                logger.info(f"Sent notification for {len(added)} new products")
            except Exception as e:
                logger.error(f"Failed to send added notification: {e}")

        # Send a single notification for all modified products
        if modified:
            try:
                modified_message = "🔄 **Products Modified!**\n\n"
                for product, changes in modified:
                    modified_message += f"📦 **{product.name}**\n"
                    for field, (old, new) in changes.items():
                        modified_message += f"🔹 {field.capitalize()}: {old} ➡️ {new}\n"
                    modified_message += f"🔗 [Product Link]({product.link})\n\n"
                    # Ensure message stays within Discord's limit
                    if len(modified_message) > DISCORD_MESSAGE_LIMIT:
                        await notifier.send_notification(modified_message)
                        modified_message = ""  # Start a new message

                if modified_message:
                    await notifier.send_notification(modified_message)

                logger.info(f"Sent notification for {len(modified)} modified products")
            except Exception as e:
                logger.error(f"Failed to send modified notification: {e}")

        # Send a single notification for all deleted products
        if deleted:
            deleted_message = "🗑️ **Products Removed!**\n\n"
            for product in deleted:
                deleted_message += f"📦 **{product.name}**\n"
                deleted_message += f"💰 Price: {product.price}\n"
                # Ensure message stays within Discord's limit
                if len(deleted_message) > DISCORD_MESSAGE_LIMIT:
                    await notifier.send_notification(deleted_message)
                    deleted_message = ""

        # Random delay between checks
        delay = random.randint(60, 300)
        logger.info(f"Waiting {delay} seconds before the next check...")

        # Visual progress bar during delay
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
    # new_scrape = scrape_all()
    # check_for_changes(new_scrape)
    notifier.run_with_task(check_changes_and_notify)
