import subprocess

from links_parser.parser import ScrapVacancySite
from dataclasses import dataclass, field
from typing import Dict

@dataclass
class DouURLs:
    base_url: str = "https://jobs.dou.ua/"
    pages_urls: Dict[str, str] = field(default_factory=lambda: {
        "dou_python": "vacancies/?category=Python",
    })

def get_dou_links() -> None:
    """Save all page links to corresponding .txt files"""
    urls = DouURLs()
    site = ScrapVacancySite()
    try:
        pages = site.get_pages(urls.base_url, urls.pages_urls)
        for page_name, page_url in pages.items():
            print(f"Processing page: {page_name}")
            site.open_page(page_url)
            site.click_more_button(css_selector="div.more-btn a")
            site.write_links_to_txt(
                f"{page_name}_links.txt",
                site.vacancies_links(css_selector="a.vt")
            )
    except Exception as error:
        print(f"Error during scraping: {error}")
    site.close_browser()

if __name__ == "__main__":

    get_dou_links()
    print("Links gathered successfully.")

    print("Starting Scrapy crawler...")
    try:
        subprocess.run(
            "python -m scrapy crawl dou_spider -o data/dou.jsonl",
            check=True
        )
        print("Scrapy crawler completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Scrapy: {e}")
