import unittest
from data_analysis.techs_counting import TechnologyCounting

class TestTechnologyCounting(unittest.TestCase):
    def setUp(self):
        """Set up an instance of TechnologyCounting for testing."""
        self.file_name = "test_file.json"
        self.techs_counting = TechnologyCounting(self.file_name)

    def test_init(self):
        """Test initialization of TechnologyCounting."""
        self.assertEqual(self.techs_counting.file_name, self.file_name)
        self.assertEqual(self.techs_counting.technology_counter, {})

    def test_descriptions(self):
        """Test getting descriptions from a JSON file."""
        descriptions = self.techs_counting.descriptions()
        self.assertIsInstance(descriptions, list)
        self.assertEqual(len(descriptions), 0)  # assuming empty file

    def test_preprocess_text(self):
        """Test text preprocessing."""
        text = "This is a test description."
        preprocessed_text = self.techs_counting.preprocess_text(text)
        self.assertIsInstance(preprocessed_text, list)
        self.assertEqual(len(preprocessed_text), 5)  # assuming 5 words

    def test_tokenized_descriptions(self):
        """Test tokenizing descriptions."""
        tokenized_descriptions = self.techs_counting.tokenized_descriptions()
        self.assertIsInstance(tokenized_descriptions, list)
        self.assertEqual(len(tokenized_descriptions), 0)  # assuming empty file

    def test_technology_counting(self):
        """Test counting technologies in descriptions."""
        self.techs_counting.technology_counting()
        self.assertIsInstance(self.techs_counting.technology_counter, dict)
        self.assertEqual(len(self.techs_counting.technology_counter), 0)  # assuming empty file

if __name__ == "__main__":
    unittest.main()
