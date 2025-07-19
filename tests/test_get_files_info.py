# When executed directly, it should run the get_files_info with the following paramaters.
import os
import sys
import unittest

# Add the project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from functions.get_files_info import get_files_info


class TestGetFilesInfo(unittest.TestCase):
    def setUp(self):
        self.working_directory = os.path.dirname(os.path.abspath(__file__))

    def test_valid_directory_dot(self):
        directory = "."
        # Should not raise and should return a list
        result = get_files_info(self.working_directory, directory)
        self.assertIsInstance(result, list)
        self.assertTrue(any("main.py: file_size=" in f for f in result))

    def test_valid_subdirectory(self):
        directory = "pkg"
        # Should not raise and should return a list
        result = get_files_info(self.working_directory, directory)
        self.assertIsInstance(result, list)
        self.assertTrue(any("render.py: file_size=" in f for f in result))

    def test_directory_outside(self):
        directory = "/bin"
        result = get_files_info(self.working_directory, directory)
        self.assertIsInstance(result, list)
        self.assertTrue(
            any(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                in f
                for f in result
            )
        )

    def test_parent_directory(self):
        directory = "../"
        result = get_files_info(self.working_directory, directory)
        self.assertIsInstance(result, list)
        self.assertTrue(
            any(
                f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
                in f
                for f in result
            )
        )


if __name__ == "__main__":
    unittest.main()
