import unittest
from unittest.mock import MagicMock, patch
from collections import Counter
from data_analysis.data_counting import VacanciesDataCounting

class TestTechnologyCounting(unittest.TestCase):

    def setUp(self):
        """Set up an instance of TechnologyCounting for testing."""
        self.tech_counter = VacanciesDataCounting("input_file.txt")
        self.tech_counter.technology_counter = Counter({
            "Python": 10,
            "JavaScript": 7,
            "HTML": 5
        })

    @patch("builtins.open")
    @patch("csv.writer")
    def test_save_to_csv(self, mock_csv_writer, mock_open):
        """Test saving results to a CSV file."""
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Mocking csv writer
        mock_writer = MagicMock()
        mock_csv_writer.return_value = mock_writer

        # Call the method
        test_output_file = "test_output.csv"
        self.tech_counter.save_to_csv(test_output_file)

        # Assert the file is opened with the correct path
        expected_file_path = self.tech_counter.get_file_path(
            "counting", test_output_file
        )
        mock_open.assert_called_once_with(
            expected_file_path, "w", newline="", encoding="utf-8"
        )

        # Assert the CSV writer is called with correct data
        mock_writer.writerow.assert_any_call(["Technology", "Frequency"])
        mock_writer.writerow.assert_any_call(["Python", 10])
        mock_writer.writerow.assert_any_call(["JavaScript", 7])
        mock_writer.writerow.assert_any_call(["HTML", 5])
        self.assertEqual(mock_writer.writerow.call_count, 4)  # Header + 3 rows

if __name__ == "__main__":
    unittest.main()
