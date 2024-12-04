import os
import subprocess

from links_parser.parser import ScrapVacancySite
# from links_parser.parser import get_all_links

def get_all_links() -> None:
    """Save all pages to corresponding .txt files"""
    site_to_scrap = ScrapVacancySite()
    try:
        site_to_scrap.scrap_pages()
    except Exception as error:
        print(f"Error during scraping: {error}")
        site_to_scrap.close_browser()


if __name__ == "__main__":

    get_all_links()
    print("Links gathered successfully.")

    # print("Starting Scrapy crawler...")
    # try:
    #     subprocess.run(
    #         ["scrapy", "crawl", "dou_spider", "-o", "data/dou.jsonl"], check=True
    #     )
    #     print("Scrapy crawler completed successfully.")
    # except subprocess.CalledProcessError as e:
    #     print(f"Error while running Scrapy: {e}")
