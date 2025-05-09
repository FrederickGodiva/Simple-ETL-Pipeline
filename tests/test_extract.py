import unittest
from unittest.mock import patch, MagicMock

from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError

from utils.extract import fetching_content, extract_fashion_data, scrape

# Sample HTML for testing
SAMPLE_HTML = """
<div class="collection-card">
    <div style="position: relative;">
        <img src="https://picsum.photos/280/350?random=2" class="collection-image" alt="T-shirt 2">
    </div>
    <div class="product-details">
        <h3 class="product-title">T-shirt 2</h3>
        <div class="price-container"><span class="price">$102.15</span></div>
            <p style="font-size: 14px; color: #777;">Rating: ⭐ 3.9 / 5</p>
            <p style="font-size: 14px; color: #777;">3 Colors</p>
            <p style="font-size: 14px; color: #777;">Size: M</p>
            <p style="font-size: 14px; color: #777;">Gender: Women</p>
        </div>
</div>
"""


class TestScraper(unittest.TestCase):

    def test_extract_fashion_data_success(self):
        soup = BeautifulSoup(SAMPLE_HTML, "html.parser")
        product = soup.select_one(".collection-card")
        result = extract_fashion_data(product)

        self.assertIsInstance(result, dict)
        self.assertEqual(result["Title"], "T-shirt 2")
        self.assertEqual(result["Price"], "$102.15")
        self.assertEqual(result["Rating"], "Rating: ⭐ 3.9 / 5")
        self.assertEqual(result["Colors"], "3 Colors")
        self.assertEqual(result["Size"], "Size: M")
        self.assertEqual(result["Gender"], "Gender: Women")
        self.assertIn("Timestamp", result)

    @patch("utils.extract.requests.get")
    def test_fetching_content_success(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html></html>"
        mock_get.return_value = mock_response

        url = "http://example.com"
        result = fetching_content(url)

        self.assertEqual(result, b"<html></html>")
        mock_get.assert_called_once_with(url, headers=mock_get.call_args[1]["headers"])

    @patch("utils.extract.fetching_content")
    def test_fetching_content_failure(self, mock_fetching):
        mock_fetching.side_effect = ConnectionError("Connection error")

        url = "https://example.co"
        result = fetching_content(url)

        self.assertIsNone(result)

    @patch("utils.extract.fetching_content")
    def test_scrape_single_page(self, mock_fetching):
        html = f"<html><body>{SAMPLE_HTML}</body></html>"
        mock_fetching.return_value = html.encode("utf-8")

        results = scrape(base_url="http://example.com/", max_pages=1, delay=0)

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["Title"], "T-shirt 2")

    @patch("utils.extract.fetching_content")
    def test_scrape_stops_on_no_content(self, mock_fetching):
        mock_fetching.return_value = None
        results = scrape(base_url="http://example.com/", max_pages=3, delay=0)

        self.assertEqual(results, [])


if __name__ == "__main__":
    unittest.main()
