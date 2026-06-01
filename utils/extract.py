from datetime import datetime
import time
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://fashion-studio.dicoding.dev"


def get_page_url(page_number: int) -> str:
    if page_number == 1:
        return BASE_URL
    return f"{BASE_URL}/page{page_number}"


def fetch_page(url: str) -> str | None:
    try:
        response = requests.get(
            url,
            timeout=30,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                )
            },
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as error:
        print(f"Error fetching website: {error}")
        return None


def find_detail_text(detail_tags, prefix: str) -> str | None:
    try:
        for tag in detail_tags:
            text = tag.get_text(strip=True)
            if text.startswith(prefix):
                return text
        return None
    except Exception as error:
        print(f"Error finding detail text: {error}")
        return None


def parse_product_card(card, timestamp: str) -> dict | None:
    try:
        title_tag = card.find("h3", class_="product-title")
        price_tag = card.select_one(".price")
        detail_tags = card.find_all("p")

        if not title_tag or not price_tag:
            return None

        rating_value = find_detail_text(detail_tags, "Rating:")
        size_value = find_detail_text(detail_tags, "Size:")
        gender_value = find_detail_text(detail_tags, "Gender:")

        colors_value = None
        for tag in detail_tags:
            text = tag.get_text(strip=True)
            if "Colors" in text:
                colors_value = text
                break

        return {
            "Title": title_tag.get_text(strip=True),
            "Price": price_tag.get_text(strip=True),
            "Rating": rating_value,
            "Colors": colors_value,
            "Size": size_value,
            "Gender": gender_value,
            "timestamp": timestamp,
        }
    except Exception as error:
        print(f"Error parsing product card: {error}")
        return None


def scrape_page(page_number: int) -> list[dict]:
    url = get_page_url(page_number)
    html = fetch_page(url)

    if not html:
        return []

    try:
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.select(".collection-card")

        timestamp = datetime.now().isoformat()
        products = []

        for card in cards:
            product = parse_product_card(card, timestamp)
            if product:
                products.append(product)

        print(f"Page {page_number}: {len(products)} products")
        return products
    except Exception as error:
        print(f"Error scraping page {page_number}: {error}")
        return []


def scrape_main(start_page: int = 1, end_page: int = 50) -> list[dict]:
    all_products = []

    try:
        for page_number in range(start_page, end_page + 1):
            page_products = scrape_page(page_number)
            all_products.extend(page_products)
            time.sleep(0.2)

        return all_products
    except Exception as error:
        print(f"An error occurred during scraping: {error}")
        return all_products