from discord_bot import DiscordNotifier
from dotenv import load_dotenv
import asyncio
import os

if __name__ == "__main__":
    load_dotenv()
    notifier = DiscordNotifier(
        os.getenv("DISCORD_TOKEN"), int(os.getenv("DISCORD_CHANNEL_ID"))
    )

    async def example_task():
        await asyncio.sleep(5)
        await notifier.send_notification("Example task completed.")

    notifier.run_with_task(example_task)
