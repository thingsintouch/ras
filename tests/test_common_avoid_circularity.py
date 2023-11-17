from decouple import config
import sys
print(sys.path)
sys.path.insert(0, config("ROOT_DIRECTORY"))

import unittest
import tempfile

from common.common_avoid_circularity import insert_line_at_top
from unittest.mock import mock_open, patch

class TestInsertLineAtTop(unittest.TestCase):
    def setUp(self):
        # Create a temporary file for testing
        self.temp_file = tempfile.NamedTemporaryFile(mode='w+', encoding='utf-8')
        self.temp_file_path = self.temp_file.name

    def tearDown(self):
        # Close and remove the temporary file after the test
        self.temp_file.close()

    def test_insert_line_at_top_success(self):
        # Test inserting a line into an existing file
        existing_content = "Existing line 1\nExisting line 2\n"
        self.temp_file.write(existing_content)
        self.temp_file.seek(0) # Move the file pointer to the beginning

        line_to_insert = "New line\n"
        insert_line_at_top(self.temp_file_path, line_to_insert)

        self.temp_file.seek(0) # Move the file pointer to the beginning
        updated_content = self.temp_file.read()

        expected_content = line_to_insert + existing_content   
        self.assertEqual(updated_content, expected_content)

    def test_insert_line_at_top_file_not_found(self):
        # Test handling FileNotFountError
        line_to_insert = "New line\n"
        insert_line_at_top(self.temp_file_path, line_to_insert)

        self.temp_file.seek(0) # Move the file pointer to the beginning
        content = self.temp_file.read()

        self.assertEqual(content, line_to_insert)

    def test_insert_line_at_top_catch_exception(self):
        # Create a mock file object that raises an exception
        mock_file = mock_open()
        mock_file.side_effect = IOError("Mock file error")

        # Use patch to replace the built-in open function with the mock file object
        with patch("builtins.open", mock_file):
            # Capture the print output
            with patch("builtins.print") as mock_print:
                # Call the insert_line_at_top function with the mock file object
                insert_line_at_top("mock_file.txt", "New line")

        # Check if the expected error message appears in the captured output
        mock_print.assert_any_call("could not write line at top of file - Exception: Mock file error")

if __name__ == '__main__':
    unittest.main()