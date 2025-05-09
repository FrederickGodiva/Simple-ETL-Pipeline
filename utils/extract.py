import time
from datetime import datetime

import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}


def fetching_content(url):
    """
    Fetches the HTML content of a given URL using a GET request.

    Args:
        url (str): The target URL to fetch.

    Returns:
        bytes or None: The raw HTML content if successful, otherwise None.
    """
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        return response.content
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Failed to fetch {url}: {e}")
        return None


def extract_fashion_data(product):
    """
    Extracts fashion product information from a BeautifulSoup HTML element.

    Args:
        product (bs4.element.Tag): The HTML block representing a product.

    Returns:
        dict or None: A dictionary containing product details such as title,
                      price, rating, colors, size, gender, and a timestamp.
                      Returns None if extraction fails.
    """
    try:
        # Extract core product details
        title = product.select_one(".product-title").get_text(strip=True)
        price = product.select_one(".price").get_text(strip=True)

        # Optional fields with default None
        rating = colors = size = gender = None

        # Loop through paragraph tags for additional details
        for tag in product.select(".product-details p"):
            text = tag.get_text(strip=True)
            if text.startswith("Rating:"):
                rating = text
            elif "Colors" in text:
                colors = text
            elif "Size:" in text:
                size = text
            elif "Gender:" in text:
                gender = text

        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        print(f"[ERROR] Failed to extract product data: {e}")
        return None


def scrape(base_url, max_pages, delay):
    """
    Iteratively scrapes multiple pages of fashion product listings.

    Args:
        base_url (str): The base URL of the site to scrape (must end with a slash if pagination appends `page{n}`).
        max_pages (int): The maximum number of pages to scrape.
        delay (int or float): Time in seconds to wait between page requests.

    Returns:
        list: A list of dictionaries, each representing a product and its details.
    """
    all_products = []

    for page in range(1, max_pages + 1):
        # Construct the paginated URL
        url = base_url if page == 1 else f"{base_url}page{page}"
        print(f"[INFO] Scraping page: {url}")

        # Fetch and parse HTML content
        content = fetching_content(url)
        if not content:
            print(f"[INFO] Stopping scrape. No content on page {page}.")
            break

        soup = BeautifulSoup(content, "html.parser")
        product_cards = soup.select(".collection-card")

        # Extract data from each product card
        for product in product_cards:
            product_data = extract_fashion_data(product)
            if product_data:
                all_products.append(product_data)

        # Respectful delay to avoid hammering the server
        time.sleep(delay)

    return all_products
