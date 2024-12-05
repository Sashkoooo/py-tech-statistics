import time
from pathlib import Path

from selenium.common import (
    TimeoutException,
    ElementClickInterceptedException,
    NoSuchElementException
)
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

        options = [
            "--headless=new",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--blink-settings=imagesEnabled=false",
            "--disable-extensions"
        ]
        for opt in options:
            opts.add_argument(opt)

        self.driver = Chrome(options=opts)

    def close_browser(self) -> None:
        print("Close browser")
        self.driver.quit()

    def open_page(self, page_url: str) -> None:
        self.driver.get(page_url)

    @staticmethod
    def get_pages(base_url: str, pages_urls: dict) -> dict[str, str]:
        return {
            page_name: urljoin(base_url, page_url)
            for page_name, page_url in pages_urls.items()
        }

    def click_more_button(self, css_selector:str) -> None:
        while True:
            try:
                more_button = self.more_button(css_selector)
                print("Click button...")
                more_button.click()
                time.sleep(0.5)

            except TimeoutException:
                print("No more buttons available (timeout waiting for button).")
                break
            except ElementClickInterceptedException:
                print("Button not clickable (intercepted by another element).")
                break
            except NoSuchElementException:
                print(f"No such element: {css_selector}")
                break
            except Exception as e:
                print(f"Unexpected error: {e}")
                break

    def more_button(self, css_selector):
        return WebDriverWait(self.driver, 1).until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, css_selector)
            )
        )

    @staticmethod
    def get_vacancies_links(page: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        links = [a["href"] for a in soup.select("a.vt") if a.get("href")]
        return links

    def write_links_to_txt(self, page: str, filename: str):
        file_path = self.get_file_path(filename)
        links = self.get_vacancies_links(page)

        try:
            with open(file_path, "w") as file:
                print("writing file")
                file.writelines(f"{link}\n" for link in links)
            print(f"Collected {len(links)} links in {filename}.")
        except IOError as error:
            print(f"Failed to write links to {filename}: {error}")

    @staticmethod
    def get_file_path(filename):
        base_dir = Path.cwd()
        file_path = base_dir / "data" / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path.resolve()

    def create_links_list(self) -> None:
        pages = self.get_pages(BASE_URL, PAGES_URLS)
        for page_name, page_url in pages.items():
            print(f"Processing page: {page_name}")
            self.open_page(page_url)
            self.click_more_button(css_selector="div.more-btn a")
            self.write_links_to_txt(
                self.driver.page_source,
                f"{page_name}_links.txt"
            )
            print(f"Data collected for {page_name}.")
        self.close_browser()
