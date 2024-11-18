import scrapy
from typing import Any
from scrapy.http import Response
from scrape_sites.items import ScrapeSitesItem


class DouSpider(scrapy.Spider):
    """Scrape pages from https://jobs.dou.ua/vacancies/?category=Python"""

    name = "dou_spider"
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    def parse(self, response: Response, **kwargs: Any) -> Any:
        vacancy_page_links = response.css(".vt ::attr(href)").getall()
        yield from response.follow_all(vacancy_page_links, self.parse_vacancy_page)

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
