def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory

    # 2 If the directory argument is outside the working_directory, return a string with an error
    if not directory.startswith(working_directory):
        raise ValueError(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )

    if not os.path.exists(directory):
        raise ValueError(f'Error: Directory "{directory}" does not exist')

    # 3 If the directory argument is not a directory, again, return an error string
    if not os.path.isdir(directory):
        raise ValueError(f'Error: "{directory}" is not a directory')

    import os

    # 4 Build and return a string representing the contents of the directory.
    # 5 If any errors are raised by the standard library functions, catch them and instead return a string describing the error. Always prefix error strings with "Error:".
    files_info = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            try:
                file_info = f"{filename}: file_size={os.path.getsize(file_path)} bytes, is_dir={os.path.isdir(file_path)}"
                files_info.append(file_info)
            except Exception as e:
                return f"Error: {str(e)}"

    return files_info
