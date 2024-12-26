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
    on_website = ScrapVacancySite()
    try:
        pages = on_website.get_pages(urls.base_url, urls.pages_urls)
        for page_name, page_url in pages.items():
            print(f"Processing page: {page_name}")
            on_website.open_page(page_url)
            on_website.click_more_button(css_selector="div.more-btn a")
            on_website.write_links_to_txt(
                f"{page_name}_links.txt",
                on_website.vacancies_links(css_selector="a.vt")
            )
    except Exception as error:
        print(f"Error during scraping: {error}")
    on_website.close_browser()