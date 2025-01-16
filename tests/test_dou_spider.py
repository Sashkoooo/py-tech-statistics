import os
import unittest
from scrapy.http import HtmlResponse, Request
from scrape_sites.spiders.dou_spider import DouSpider


class TestDouSpider(unittest.TestCase):
    def setUp(self):
        """Set up a DouSpider instance and mock data for tests."""
        self.spider = DouSpider()
        self.mock_vacancy_page = """
        <html>
            <body>
                <h1 class="g-h2">Python Developer</h1>
                <div class="l-n">
                    <a>Awesome Company</a>
                </div>
                <div class="b-typo vacancy-section">
                    <p>Experience in Python, Django, Flask.</p>
                    <p>Remote work available.</p>
                </div>
            </body>
        </html>
        """
        self.mock_empty_page = "<html><body></body></html>"

    def test_clean_text(self) -> None:
        """Test the clean_text method."""
        raw_description = ["Hello\xa0World!", "Python\u202fDeveloper", "Good\u200bjob!"]
        cleaned_text = self.spider.clean_text(raw_description)
        print(cleaned_text)
        expected_output = "Hello World! Python Developer Goodjob!"
        self.assertEqual(cleaned_text, expected_output)

    def test_parse_vacancy_page(self) -> None:
        """Test the parse_vacancy_page method with a valid response."""
        # Simulate a response object for the vacancy page
        request = Request(url="https://example.com/vacancy/1")
        response = HtmlResponse(
            url=request.url,
            request=request,
            body=self.mock_vacancy_page,
            encoding="utf-8",
        )

        # Call parse_vacancy_page and check the result
        results = list(self.spider.parse_vacancy_page(response))
        self.assertEqual(len(results), 1)  # Ensure one item is returned

        item = results[0]
        self.assertEqual(item["title"], "Python Developer")
        self.assertEqual(item["company"], "Awesome Company")
        self.assertEqual(
            item["description"], "Experience in Python, Django, Flask. Remote work available."
        )
        self.assertEqual(item["url"], "https://example.com/vacancy/1")

    def test_parse_empty_vacancy_page(self):
        """Test parse_vacancy_page with an empty response."""
        # Simulate a response object for an empty page
        request = Request(url="https://example.com/vacancy/2")
        response = HtmlResponse(
            url=request.url,
            request=request,
            body=self.mock_empty_page,
            encoding="utf-8",
        )

        # Call parse_vacancy_page and check the result
        results = list(self.spider.parse_vacancy_page(response))
        self.assertEqual(len(results), 1)  # Ensure one item is returned

        item = results[0]
        self.assertEqual(item["title"], "No title provided")
        self.assertEqual(item["company"], "No company provided")
        self.assertEqual(item["description"], "")
        self.assertEqual(item["url"], "https://example.com/vacancy/2")

    def test_start_requests_valid_file(self):
        """Test start_requests with a valid file."""
        # Create a temporary test file with some URLs
        test_file_path = "data/links/dou_python_links.txt"
        os.makedirs(os.path.dirname(test_file_path), exist_ok=True)
        with open(test_file_path, "w") as file:
            file.write("https://example.com/vacancy/1\n")
            file.write("https://example.com/vacancy/2\n")

        try:
            requests = list(self.spider.start_requests())
            self.assertEqual(len(requests), 2)  # Two requests should be yielded
            self.assertEqual(requests[0].url, "https://example.com/vacancy/1")
            self.assertEqual(requests[1].url, "https://example.com/vacancy/2")
        finally:
            # Clean up the test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)


if __name__ == "__main__":
    unittest.main()
