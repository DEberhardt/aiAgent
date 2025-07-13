# When executed directly, it should run the get_files_info with the following paramaters. We added some examples of the expected output.
import os
from functions.get_files_info import get_files_info
import sys

if __name__ == "__main__":
    working_directory = os.path.dirname(os.path.abspath(__file__))
    print(get_files_info(working_directory))


