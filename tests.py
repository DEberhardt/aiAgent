# When executed directly, it should run the get_files_info with the following paramaters.
import os
from functions.get_files_info import get_files_info


# Should not raise and should return a list
get_files_info("calculator", ".")

# Should not raise and should return a list
get_files_info("calculator", "pkg")

# Should raise ValueError for directory outside working dir
get_files_info("calculator", "/bin")

# Should raise ValueError for parent directory
get_files_info("calculator", "../")
