import time
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urljoin
from bs4 import BeautifulSoup

BASE_URL = "https://jobs.dou.ua/"
PAGES_URLS = {
    "dou_python": "vacancies/?category=Python",
}

class ScrapVacancySite:
    """Class to scrap vacancy site"""
    def __init__(self) -> None:
        print("Open browser")
        opts = Options()
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--blink-settings=imagesEnabled=false")
        opts.add_argument("--disable-extensions")
        self.driver = Chrome(options=opts)

    def close_browser(self) -> None:
        print("Close browser")
        self.driver.close()

    def open_page(self, page_url: str) -> None:
        self.driver.get(page_url)

    @staticmethod
    def get_pages() -> dict[str, str]:
        return {
            page_name: urljoin(BASE_URL, page_url)
            for page_name, page_url in PAGES_URLS.items()
        }

    def click_more_button(self):
        pass

    def scrap_pages(self) -> None:
        pages = self.get_pages()

        for page_name, page_url in pages.items():
            print(f"Processing page: {page_name}")
            self.open_page(page_url)
            self.click_more_button()
            VacancyLinksParser(self.driver.page_source).write_links_to_txt()
            print("Collecting data...")

        self.close_browser()


class ScrapDouSite(ScrapVacancySite):
    """Class to scrap Dou vacancy site"""
    def click_more_button(self) -> None:
        while True:
            try:
                more_button = WebDriverWait(self.driver, 1).until(
                    ec.element_to_be_clickable(
                        (By.CSS_SELECTOR, "div.more-btn a")
                    )
                )
                print("Click button...")
                more_button.click()
                time.sleep(0.5)
            except Exception:
                print("No more buttons available")
                break

class VacancyLinksParser:
    """Class to parse vacancies links and write them into text file"""
    def __init__(self, page: str) -> None:
        self.page_source = page

    def get_page_soup(self) -> BeautifulSoup:
        return BeautifulSoup(self.page_source, "html.parser")

    def get_vacancies_links(self) -> list[str]:
        soup = self.get_page_soup()
        links = [a["href"] for a in soup.select("a.vt") if a.get("href")]
        return links

    def write_links_to_txt(self):
        with open("links.txt", "w") as f:
            for link in self.get_vacancies_links():
                f.write(link + "\n")
        print(f"Collected {len(self.get_vacancies_links())} links.")

def get_all_links() -> None:
    """Save all pages to corresponding .csv files"""
    site_to_scrap = ScrapDouSite()
    site_to_scrap.scrap_pages()


if __name__ == "__main__":
    get_all_links()
