import subprocess

from data_analysis.data_handling import python_techs_handling
from links_parser.urls_handling import get_dou_links


if __name__ == "__main__":

    get_dou_links()
    print("Dou.ua links gathered successfully.")

    print("Starting Scrapy crawler...")
    try:
        subprocess.run(
            "python -m scrapy crawl dou_spider -O data/source/dou.jsonl",
            check=True
        )
        print("Scrapy crawler completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Scrapy: {e}")

    python_techs_handling("dou.jsonl")

