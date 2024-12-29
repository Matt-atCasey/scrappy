import discord
import asyncio


class DiscordNotifier:
    def __init__(self, token: str, channel_id: int):
        """
        Initialize the DiscordNotifier.

        :param token: Your Discord bot token.
        :param channel_id: The ID of the Discord channel to send messages to.
        """
        self.token = token
        self.channel_id = channel_id
        self.client = discord.Client(intents=discord.Intents.default())

    async def send_notification(self, message: str):
        """
        Send a notification to the specified Discord channel.

        :param message: The message to send.
        """
        if not self.client.is_ready():
            print("Client is not ready. Ensure the bot is properly initialized.")
            return

        channel = self.client.get_channel(self.channel_id)
        if channel:
            try:
                embed = discord.Embed(
                    title="New Update", description=message, color=discord.Color.blue()
                )
                await channel.send(embed=embed)
            except discord.Forbidden:
                print("Bot does not have permission to send messages to the channel.")
            except discord.HTTPException as e:
                print(f"Failed to send message due to an HTTP error: {e}")
        else:
            print(
                f"Channel with ID {self.channel_id} not found. Ensure the ID is correct and the bot has access."
            )

    def start(self):
        """
        Start the Discord bot.
        """

        @self.client.event
        async def on_ready():
            print(f"Bot is ready! Logged in as {self.client.user}")

        # Run the bot
        self.client.run(self.token)

    def run_with_task(self, task):
        @self.client.event
        async def on_ready():
            print(f"Bot is ready! Logged in as {self.client.user}")
            # Call the task coroutine explicitly
            self.client.loop.create_task(task())

        self.client.run(self.token)
