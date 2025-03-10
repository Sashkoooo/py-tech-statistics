import json
import re
import nltk
import csv
from typing import Any
from nltk.tokenize import word_tokenize
from pathlib import Path
from collections import Counter
from data_analysis.config import technology_groups
from datetime import datetime

nltk.download("punkt")


class VacanciesDataCounting:
    """Class to count data within vacancies source file"""
    def __init__(self, source_file_name: str) -> None:
        self.file_name = source_file_name
        self.technology_counter = Counter()
        self.file_content = self.open_file()
        self.technology_counting()
        self.senior = 0
        self.middle = 0
        self.junior = 0
        self.not_specified = 0

    @staticmethod
    def get_file_path(folder: str, file_name: str) -> Path:
        """Get file path"""
        base_dir = Path.cwd()
        file_path = base_dir / "data" / folder / file_name
        return file_path.resolve()

    def open_file(self) -> None | list[Any] | list[str]:
        """Open file"""
        try:
            with open(
                    self.get_file_path("source", self.file_name), "r", encoding="utf-8"
            ) as file:
                print("File opened successfully.")
                return file.readlines()
        except FileNotFoundError:
            print(f"File {self.file_name} is not found.")
            return []
        except IOError:
            print(f"Error opening file {self.file_name}.")
            return []

    def get_data_from_jsonl(self, column_name: str) -> list[Any]:
        """Get data from jsonl file"""
        output = []
        lines = self.file_content
        for line in lines:
            data = json.loads(line)
            output.append(data.get(column_name, ""))
        return output

    def titles_number(self) -> int:
        """Get number of titles"""
        return len(self.get_data_from_jsonl(column_name="title"))

    def count_positions(self) -> None:
        """Count positions"""
        for position in self.get_data_from_jsonl(column_name="title"):
            if "senior" in position.lower():
                self.senior += 1
            elif "middle" in position.lower():
                self.middle += 1
            elif "junior" in position.lower():
                self.junior += 1
            else:
                self.not_specified +=1

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
            self.preprocess_text(description)
            for description in self.get_data_from_jsonl(column_name="description")
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
                self.get_file_path("counting", output_file), "w", newline="", encoding="utf-8"
        ) as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Technology", "Frequency"])
            for tech, count in self.technology_counter.items():
                writer.writerow([tech, count])

        print(f"The results are saved to: {output_file}")
