# When executed directly, it should run the get_files_info with the following paramaters.
import os

# Testing get_files_info function with various cases
from functions.get_files_info import get_files_info

# # Should not raise and should return a list
# get_files_info("calculator", ".")

# # Should not raise and should return a list
# get_files_info("calculator", "pkg")

# # Should raise ValueError for directory outside working dir
# get_files_info("calculator", "/bin")

# # Should raise ValueError for parent directory
# get_files_info("calculator", "../")


# Testing get_file_content function with various cases
from functions.get_file_content import get_file_content

# # Testing get_file_content function with truncation
# get_file_content("calculator", "lorem.txt")

# # Should return a string with file content
# get_file_content("calculator", "main.py")

# # Should return a string with file content
# get_file_content("calculator", "pkg/calculator.py")

# # Should return an Error string for a file outside the working directory
# get_file_content("calculator", "/bin/cat")

# # Should return an Error string for a file not found
# get_file_content("calculator", "pkg/does_not_exist.py")


# Testing write_file function with various cases
from functions.write_file import write_file

# # Should overwrite the content of the existing file
# write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

# # Should create a file and write this text to it
# write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

# # Should fail because file does not exist
# write_file("calculator", "/tmp/temp.txt", "this should not be allowed")


# Testing run_python_file function with various cases
from functions.run_python_file import run_python_file

# # This should print the calculator's usage instructions
# run_python_file("calculator", "main.py")

# # Should run the calculator with a different working directory
# # (should run the calculator... which gives a kinda nasty rendered result)
# run_python_file("calculator", "main.py", ["3 + 5"])

# # This should run the calculator tests
# run_python_file("calculator", "tests.py")

# # This should return an error string
# run_python_file("calculator", "../main.py")

# # This should return an error string
# run_python_file("calculator", "nonexistent.py")

# # This should return an error string
# run_python_file("calculator", "lorem.txt")
