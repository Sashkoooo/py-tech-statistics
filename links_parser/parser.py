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
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class ScrapVacancySite:
    """Class to scrap vacancy site & create links list"""
    def __init__(self) -> None:
        self.driver = None

    def open_chrome_browser(self) -> None:
        print("Open browser")
        opts = Options()

        options = [
            "--headless=new",
            "--disable-gpu",
            "--window-size=1920,1080",
            "--blink-settings=imagesEnabled=false",
            "--disable-extensions"
        ]
        for option in options:
            opts.add_argument(option)

        self.driver = Chrome(options=opts)

    def close_browser(self) -> None:
        print("Close browser")
        self.driver.quit()

    def open_page(self, page_url: str) -> None:
        self.driver.get(page_url)

    @staticmethod
    def get_pages(base_url: str, pages_urls: dict) -> dict[str, str]:
        """Get pages urls"""
        return {
            page_name: urljoin(base_url, page_url)
            for page_name, page_url in pages_urls.items()
        }

    def click_more_button(self, css_selector:str) -> None:
        """Click more button"""
        while True:
            try:
                print("Click button...")
                self.more_button(css_selector).click()
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

    def more_button(self, css_selector) -> WebElement:
        """Get more button"""
        return WebDriverWait(self.driver, 1).until(
            ec.element_to_be_clickable(
                (By.CSS_SELECTOR, css_selector)
            )
        )

    def page_soup(self) -> BeautifulSoup:
        """Parse page source"""
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def vacancies_links(self, css_selector: str) -> list[str]:
        """Get links from page source"""
        links = [
            url["href"] for url in self.page_soup().select(css_selector)
            if url.get("href")
        ]
        return links

    def write_links_to_txt(self, filename: str, links: list[str]) -> None:
        """Write links to file"""
        try:
            with open(self.file_path(filename), "w") as file:
                print("writing file")
                file.writelines(f"{link}\n" for link in links)
            print(f"Collected {len(links)} links in {filename}.")
        except IOError as error:
            print(f"Failed to write links to {filename}: {error}")

    @staticmethod
    def file_path(filename: str) -> Path:
        base_dir = Path.cwd()
        file_path = base_dir / "data/links" / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        return file_path.resolve()
