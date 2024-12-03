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
        opts.add_argument("--headless=new")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--window-size=1920,1080")
        opts.add_argument("--blink-settings=imagesEnabled=false")
        opts.add_argument("--disable-extensions")
        self.driver = Chrome(options=opts)

    def close_browser(self) -> None:
        print("Close browser")
        self.driver.quit()

    def open_page(self, page_url: str) -> None:
        self.driver.get(page_url)

    @staticmethod
    def get_pages() -> dict[str, str]:
        return {
            page_name: urljoin(BASE_URL, page_url)
            for page_name, page_url in PAGES_URLS.items()
        }

    def scrap_pages(self) -> None:
        pages = self.get_pages()
        for page_name, page_url in pages.items():
            print(f"Processing page: {page_name}")
            self.open_page(page_url)
            self.click_more_button()
            self.start_vacancy_links_parser(page_name)
            print(f"Data collected for {page_name}.")
        self.close_browser()

    def start_vacancy_links_parser(self, page_name):
        """Method should be overridden in child classes"""
        pass
        # VacancyLinksParser.write_links_to_txt(
        #     self.driver.page_source, f"{page_name}_links.txt"
        # )

    def click_more_button(self):
        """Method should be overridden in child classes"""
        pass

    def click_button_with_retries(self, css_selector:str) -> None:
        while True:
            try:
                more_button = WebDriverWait(self.driver, 1).until(
                    ec.element_to_be_clickable(
                        (By.CSS_SELECTOR, css_selector)
                    )
                )
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


class ScrapDouSite(ScrapVacancySite):
    def __init__(self):
        super().__init__()

    """Class to scrap DOU vacancy site"""
    def click_more_button(self) -> None:
        while self.click_button_with_retries("div.more-btn a"):
            pass

    def start_vacancy_links_parser(self, page_name):
        VacancyLinksParser.write_links_to_txt(
            self.driver.page_source, f"{page_name}_links.txt"
        )


class VacancyLinksParser:
    """Class to parse vacancies links and write them into text file"""

    @staticmethod
    def get_vacancies_links(page: str) -> list[str]:
        soup = BeautifulSoup(page, "html.parser")
        links = [a["href"] for a in soup.select("a.vt") if a.get("href")]
        return links
        pass

    @staticmethod
    def write_links_to_txt(page: str, filename: str):
        base_dir = Path.cwd()
        print(f"base dir{base_dir}")
        file_path = base_dir / "data" / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)
        absolute_file_path = file_path.resolve()
        print(f"absolute file path: {absolute_file_path}")
        links = VacancyLinksParser.get_vacancies_links(page)

        try:
            with open(absolute_file_path, "w") as f:
                print("writing file")
                f.writelines(f"{link}\n" for link in links)
            print(f"Collected {len(links)} links in {filename}.")
        except IOError as e:
            print(f"Failed to write links to {filename}: {e}")

# class DouVacancyLinksParser(VacancyLinksParser):
#     """Class to parse vacancies links from DOU site"""
#     @staticmethod
#     def get_vacancies_links(page: str) -> list[str]:
#         soup = BeautifulSoup(page, "html.parser")
#         links = [a["href"] for a in soup.select("a.vt") if a.get("href")]
#         return links




# def get_all_links() -> None:
#     """Save all pages to corresponding .txt files"""
#     site_to_scrap = ScrapDouSite()
#     try:
#         site_to_scrap.scrap_pages()
#     except Exception as e:
#         print(f"Error during scraping: {e}")
#         site_to_scrap.close_browser()


if __name__ == "__main__":
    get_all_links()
