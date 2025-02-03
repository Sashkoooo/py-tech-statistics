import json
import re
import nltk
import csv
from nltk.tokenize import word_tokenize
from pathlib import Path
from collections import Counter
from data_analysis.config import technology_groups
from datetime import datetime

nltk.download("punkt")


class TechnologyCounting:
    """Class to count technologies in descriptions"""
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.technology_counter = Counter()
        self.technology_counting()

    @staticmethod
    def file_path(folder: str, file_name: str) -> Path:
        """Get file path"""
        base_dir = Path.cwd()
        file_path = base_dir / "data" / folder / file_name
        return file_path.resolve()

    def descriptions(self) -> list[str]:
        """Get descriptions from json file"""
        descriptions = []
        try:
            with open(
                    self.file_path("source", self.file_name), "r", encoding="utf-8"
            ) as file:
                for line in file:
                    data = json.loads(line)
                    descriptions.append(data.get("description", ""))
        except FileNotFoundError:
            print(f"File {self.file_name} is not found.")
        except json.JSONDecodeError:
            print(f"JSON file {self.file_name} decoding error.")
        return descriptions

    @staticmethod
    def preprocess_text(text: str) -> list[str]:
        """Text preprocessing"""
        text = text.lower()
        text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)
        tokens = word_tokenize(text)
        return tokens

    def tokenized_descriptions(self) -> list[list[str]]:
        """Tokenize descriptions"""
        tokenized_descriptions = [
            self.preprocess_text(desc) for desc in self.descriptions()
        ]
        return tokenized_descriptions

    def technology_counting(self) -> None:
        """Count technologies in descriptions"""
        for tokens in self.tokenized_descriptions():
            unique_technologies = set()
            for tech, synonyms in technology_groups.items():
                if any(synonym in tokens for synonym in synonyms):
                    unique_technologies.add(tech)
            self.technology_counter.update(unique_technologies)


    def save_to_csv(self, output_file: str = None) -> None:
        """Save results to csv file"""
        if output_file is None:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
            output_file = f"techs_counting_{timestamp}.csv"

        with open(
                self.file_path("counting", output_file), "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Technology", "Frequency"])
            for tech, count in self.technology_counter.items():
                writer.writerow([tech, count])

        print(f"The results are saved to: {output_file}")
