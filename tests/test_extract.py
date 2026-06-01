from unittest.mock import Mock, patch
import requests
from bs4 import BeautifulSoup

from utils.extract import get_page_url, fetch_page, parse_product_card, scrape_main


def test_get_page_url_page_1():
    assert get_page_url(1) == "https://fashion-studio.dicoding.dev"


def test_get_page_url_page_2():
    assert get_page_url(2) == "https://fashion-studio.dicoding.dev/page2"


def test_fetch_page_success():
    mock_response = Mock()
    mock_response.text = "<html></html>"
    mock_response.raise_for_status.return_value = None

    with patch("utils.extract.requests.get", return_value=mock_response):
        result = fetch_page("https://fashion-studio.dicoding.dev")
        assert result == "<html></html>"


def test_fetch_page_request_exception():
    with patch(
        "utils.extract.requests.get",
        side_effect=requests.exceptions.RequestException("network error")
    ):
        result = fetch_page("https://fashion-studio.dicoding.dev")
        assert result is None


def test_parse_product_card_success():
    html = """
    <div class="collection-card">
        <h3 class="product-title">T-shirt 2</h3>
        <div class="price-container">
            <span class="price">$102.15</span>
        </div>
        <p>Rating: ⭐ 3.9 / 5</p>
        <p>3 Colors</p>
        <p>Size: M</p>
        <p>Gender: Women</p>
    </div>
    """

    soup = BeautifulSoup(html, "html.parser")
    card = soup.select_one(".collection-card")

    result = parse_product_card(card, "2026-06-01T17:13:33.527605")

    assert result == {
        "Title": "T-shirt 2",
        "Price": "$102.15",
        "Rating": "Rating: ⭐ 3.9 / 5",
        "Colors": "3 Colors",
        "Size": "Size: M",
        "Gender": "Gender: Women",
        "timestamp": "2026-06-01T17:13:33.527605",
    }


@patch("utils.extract.scrape_page")
def test_scrape_main_collects_all_products(mock_scrape_page):
    mock_scrape_page.side_effect = [
        [{"Title": "Product 1"}],
        [{"Title": "Product 2"}],
    ]

    result = scrape_main(1, 2)

    assert len(result) == 2
    assert result[0]["Title"] == "Product 1"
    assert result[1]["Title"] == "Product 2"