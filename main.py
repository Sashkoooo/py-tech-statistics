import subprocess

from data_analysis.techs_handling import techs_handling
from links_parser.urls_handling import get_dou_links


if __name__ == "__main__":

    get_dou_links()
    print("Links gathered successfully.")

    print("Starting Scrapy crawler...")
    try:
        subprocess.run(
            "python -m scrapy crawl dou_spider -o data/source/dou.jsonl",
            check=True
        )
        print("Scrapy crawler completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error while running Scrapy: {e}")

    techs_handling("dou.jsonl")
