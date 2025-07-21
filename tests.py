# When executed directly, it should run the get_files_info with the following paramaters.
import os
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file

# Testing get_files_info function with various cases

# # Should not raise and should return a list
# get_files_info("calculator", ".")

# # Should not raise and should return a list
# get_files_info("calculator", "pkg")

# # Should raise ValueError for directory outside working dir
# get_files_info("calculator", "/bin")

# # Should raise ValueError for parent directory
# get_files_info("calculator", "../")


# Testing get_file_content function with various cases

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

# Should overwrite the content of the existing file
write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")

# Should create a file and write this text to it
write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")

# Should fail because file does not exist
write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
