import unittest
from unittest.mock import MagicMock, patch
from pathlib import Path
from bs4 import BeautifulSoup
from selenium.common import (
    TimeoutException,
)
from links_parser.parser import ScrapVacancySite


class TestScrapVacancySite(unittest.TestCase):

    def setUp(self):
        """Set up an instance of ScrapVacancySite for testing."""
        self.scraper = ScrapVacancySite()
        self.scraper.driver = MagicMock()  # Mock Selenium WebDriver

    def tearDown(self):
        """Clean up after tests."""
        self.scraper.close_browser()

    def test_open_page(self):
        """Test opening a page."""
        page_url = "http://example.com"
        self.scraper.open_page(page_url)
        self.scraper.driver.get.assert_called_once_with(page_url)

    def test_get_pages(self):
        """Test generating full URLs from base URL and paths."""
        base_url = "http://example.com"
        pages_urls = {"page1": "/page1", "page2": "/page2"}
        expected = {"page1": "http://example.com/page1", "page2": "http://example.com/page2"}
        result = self.scraper.get_pages(base_url, pages_urls)
        self.assertEqual(result, expected)

    @patch("links_parser.parser.WebDriverWait")
    def test_click_more_button(self, mock_wait):
        """Test clicking the 'more' button."""
        mock_button = MagicMock()
        mock_wait.return_value.until.return_value = mock_button

        # Simulate the first click succeeds, then TimeoutException occurs.
        mock_button.click.side_effect = [None, TimeoutException()]

        self.scraper.click_more_button(".more-button")

        self.assertEqual(mock_button.click.call_count, 2)

    @patch("links_parser.parser.WebDriverWait")
    def test_more_button(self, mock_wait):
        """Test retrieving the 'more' button element."""
        mock_button = MagicMock()
        mock_wait.return_value.until.return_value = mock_button

        button = self.scraper.more_button(".more-button")
        self.assertEqual(button, mock_button)
        mock_wait.assert_called_once()

    def test_page_soup(self):
        """Test parsing page source into BeautifulSoup."""
        self.scraper.driver.page_source = "<html><body><p>Test</p></body></html>"
        soup = self.scraper.page_soup()
        self.assertIsInstance(soup, BeautifulSoup)
        self.assertEqual(soup.p.text, "Test")

    def test_vacancies_links(self):
        """Test extracting links from page source."""
        html = ('<html>'
                  '<body>'
                    '<a href="http://example.com/1">Link1</a>'
                    '<a href="http://example.com/2">Link2</a>'
                  '</body>'
                '</html>'
                )
        self.scraper.driver.page_source = html

        links = self.scraper.vacancies_links("a")
        expected = ["http://example.com/1", "http://example.com/2"]
        self.assertEqual(links, expected)

    @patch("builtins.open")
    def test_write_links_to_txt(self, mock_open):
        filename = "test_links.txt"
        links = ["http://example.com/1", "http://example.com/2"]

        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.scraper.write_links_to_txt(filename, links)

        mock_open.assert_called_once_with(self.scraper.file_path(filename), "w")
        mock_file.writelines.assert_called_once()
        expected_lines = [f"{link}\n" for link in links]
        actual_lines = list(mock_file.writelines.call_args[0][0])
        self.assertEqual(actual_lines, expected_lines)

    def test_file_path(self):
        """Test generating file path."""
        filename = "test_links.txt"
        expected_path = Path.cwd() / "data/links" / filename
        result = self.scraper.file_path(filename)
        self.assertEqual(result, expected_path.resolve())


if __name__ == "__main__":
    unittest.main()

