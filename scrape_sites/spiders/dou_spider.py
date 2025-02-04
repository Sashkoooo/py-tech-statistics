import scrapy
import re
from typing import Any, Generator
from scrapy.http import Response
from scrape_sites.items import ScrapeSitesItem


class DouSpider(scrapy.Spider):
    """Scrape pages from https://jobs.dou.ua/vacancies/?category=Python"""

    name = "dou_spider"

    def start_requests(self):
        # List of file paths to load links from
        file_paths = [
            "data/links/dou_python_links.txt",
            # Add more file paths as needed
        ]

        # Load links from each file
        urls = []
        for file_path in file_paths:
            with open(file_path, "r") as file:
                urls.extend(line.strip() for line in file.readlines())

        # Yield Scrapy requests
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_vacancy_page)

    def parse_vacancy_page(self, response: Response) -> Generator[ScrapeSitesItem, Any, None]:
        """Parse vacancy page"""
        vacancy = ScrapeSitesItem()
        vacancy["title"] = (
                response.css(".g-h2::text").get() or "No title provided"
        )
        vacancy["company"] = (
                response.css("div.l-n a::text").get() or "No company provided"
        )
        description = response.css("div.b-typo.vacancy-section ::text").getall()
        vacancy["description"] = self.clean_text(description)
        vacancy["url"] = response.url

        yield vacancy

    @staticmethod
    def clean_text(description: list[str]) -> str:
        """
        Clean description from unwanted characters and normalize whitespace.
        """
        unwanted_chars = {
            "\xa0": " ",  # Non-breaking space
            "\u202f": " ",  # Narrow no-break space
            "\u200b": "",  # Zero-width space
            "\n": "",
            "\t": "",
        }
        translation_table = str.maketrans(unwanted_chars)
        cleaned_text_list = [text.translate(translation_table) for text in description]
        cleaned_text_str = " ".join(cleaned_text_list).strip()

        # Normalize multiple spaces to a single space
        normalized_text = re.sub(r'\s+', ' ', cleaned_text_str)
        return normalized_text
