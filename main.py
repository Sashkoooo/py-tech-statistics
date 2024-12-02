import os
import subprocess


def get_all_links() -> None:
    """Save all pages to corresponding .txt files"""
    site_to_scrap = ScrapDouSite()
    try:
        site_to_scrap.scrap_pages()
    except Exception as error:
        print(f"Error during scraping: {error}")
        site_to_scrap.close_browser()


if __name__ == "__main__":
    # Виконати get_all_links()
    get_all_links()
    print("Links gathered successfully.")

    # Запустити Scrapy crawler
    print("Starting Scrapy crawler...")
    try:
        subprocess.run(
            ["scrapy", "crawl", "dou_spider", "-o", "output.jsonl"], check=True
        )
        print("Scrapy crawler completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Scrapy: {e}")
