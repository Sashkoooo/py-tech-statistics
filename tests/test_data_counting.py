import json
import unittest
from data_analysis.data_counting import VacanciesDataCounting


class TestVacanciesDataCounting(unittest.TestCase):
    def setUp(self):
        """Set up an instance of TechnologyCounting for testing."""
        self.file_name = "test_file.jsonl"
        self.techs_counting = VacanciesDataCounting(self.file_name)
        self.file_content = [
            {"title": "Senior Python Developer", "description": "Experience with Python and Django"},
            {"title": "Middle Java Developer", "description": "Java, Spring Framework"},
            {"title": "Junior Frontend Developer", "description": "React, JavaScript, CSS"},
            {"title": "Software Engineer", "description": "GIT, OOP, Linux"},
        ]
        self.convert_to_jsonl = [json.dumps(entry) + "\n" for entry in self.file_content]
        self.techs_counting.file_content = self.convert_to_jsonl

    def test_init(self):
        """Test initialization of TechnologyCounting."""
        self.assertEqual(self.techs_counting.file_name, self.file_name)
        self.assertEqual(self.techs_counting.technology_counter, {})

    def test_get_data_from_jsonl(self):
        """Test getting data from jsonl file."""
        data = self.techs_counting.get_data_from_jsonl("title")
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)

    def test_titles_number(self):
        """Test getting number of titles."""
        titles_number = self.techs_counting.titles_number()
        self.assertIsInstance(titles_number, int)
        self.assertEqual(titles_number, 4)

    def test_count_positions(self):
        """Test counting positions."""
        self.techs_counting.count_positions()
        self.assertEqual(self.techs_counting.senior, 1)
        self.assertEqual(self.techs_counting.middle, 1)
        self.assertEqual(self.techs_counting.junior, 1)
        self.assertEqual(self.techs_counting.not_specified, 1)

    def test_preprocess_text(self):
        """Test text preprocessing."""
        text = "This is a test description."
        preprocessed_text = self.techs_counting.preprocess_text(text)
        self.assertIsInstance(preprocessed_text, list)
        self.assertEqual(len(preprocessed_text), 5)

    def test_tokenized_descriptions(self):
        """Test tokenizing descriptions."""
        tokenized_descriptions = self.techs_counting.tokenized_descriptions()
        self.assertIsInstance(tokenized_descriptions, list)
        self.assertEqual(len(tokenized_descriptions), 4)

    def test_technology_counting(self):
        """Test counting technologies in descriptions."""
        self.techs_counting.technology_counting()
        self.assertIsInstance(self.techs_counting.technology_counter, dict)
        self.assertEqual(len(self.techs_counting.technology_counter), 10)

if __name__ == "__main__":
    unittest.main()
