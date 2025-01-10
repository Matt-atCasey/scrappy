# Scrappy

A Python-based scraper and Discord notifier for tracking changes in product listings from various online stores.

---

## Features

-   Scrapes product data from predefined URLs.
-   Detects changes such as price updates, new products, or deleted products.
-   Notifies a Discord channel about updates in real-time.
-   Uses Python-uv as the package manager for dependency management.

---

## Prerequisites

1. Python 3.10 or later installed on your system.
2. [Python-uv](https://pypi.org/project/python-uv/) installed for managing dependencies.
3. A Discord bot token with access to a channel where notifications will be sent.
4. The following Python libraries:
    - `httpx`
    - `beautifulsoup4`
    - `discord.py`
    - `rich`
    - `python-dotenv`
5. Basic knowledge of Git and GitHub if contributing to the project.

---

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/Matt-atCasey/scrappy.git
    cd scrappy
    ```

2. Install dependencies using Python-uv:

    ```bash
    uv setup
    ```

---

## Configuration

1. Create a `.env` file in the project root and add the following:

    ```env
    DISCORD_TOKEN=your_discord_bot_token
    DISCORD_CHANNEL_ID=your_discord_channel_id
    ```

2. Modify the `scrape_scan` function or other scraping methods in `scrapers.py` to include URLs for the products you want to monitor.

---

## Usage

1. Activate the Python-uv environment:

    ```bash
    uv activate
    ```

2. Run the main script:

    ```bash
    python main.py
    ```

3. The script will:

    - Scrape the predefined URLs for product data.
    - Compare the scraped data with a local `products.json` file.
    - Detect changes (new, modified, or deleted products).
    - Send notifications to the configured Discord channel.

---

## Development

1. Create a feature branch:

    ```bash
    git checkout -b feature-branch-name
    ```

2. Make your changes and commit them:

    ```bash
    git add .
    git commit -m "Description of changes"
    ```

3. Push your changes:

    ```bash
    git push origin feature-branch-name
    ```

4. Open a pull request on GitHub to merge your feature branch into `main`.

---

## Contributing

Contributions are welcome! Please follow these steps:

-   Fork the repository.
-   Create a new branch for your feature.
-   Commit your changes with clear commit messages.
-   Submit a pull request for review.

---

## Troubleshooting

1. **Error: Missing dependencies**
   Ensure you have run `uv setup` to install the required libraries.

2. **Error: Discord bot not sending messages**

    - Check that your bot token and channel ID are correctly configured in the `.env` file.
    - Ensure the bot has the necessary permissions in the Discord server.

3. **Error: Scraper not working for some URLs**

    - Verify that the URL structure has not changed.
    - Update the scraping logic if necessary.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
