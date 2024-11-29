import scrapy
from typing import Any
from scrapy.http import Response
from scrape_sites.items import ScrapeSitesItem


class DouSpider(scrapy.Spider):
    """Scrape pages from https://jobs.dou.ua/vacancies/?category=Python"""

    name = "dou_spider"

    def start_requests(self):
        # Load links from the file
        with open("links_parser/dou_python_links.txt", "r") as f:
            urls = [line.strip() for line in f.readlines()]

        # Yield Scrapy requests
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_vacancy_page)

    def parse_vacancy_page(self, response: Response, **kwargs: Any) -> None:
        """Parse vacancy page"""
        vacancy = ScrapeSitesItem()
        vacancy["title"] = response.css(".g-h2::text").get()
        vacancy["company"] = response.css("div.l-n a::text").get()
        description = response.css("div.b-typo.vacancy-section ::text").getall()
        vacancy["description"] = self.clean_text(description)
        vacancy["url"] = response.url

        yield vacancy

    @staticmethod
    def clean_text(description) -> str:
        """Clean description from non-breaking spaces in Unicode format"""
        cleaned_text_list = [text.replace("\xa0", " ") for text in description]
        cleaned_text_str = " ".join(cleaned_text_list).strip()
        return cleaned_text_str
