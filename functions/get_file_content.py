def get_file_content(working_directory, file_path):
    import os
    from config import MAX_CHARS

    abs_working_directory = os.path.abspath(working_directory)
    # print(f"Working directory: {abs_working_directory}")

    abs_file_path = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, file_path))
    )
    # print(f"File Path:         {abs_file_path}")

    if not abs_file_path.startswith(abs_working_directory):
        print(
            f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        )
        return

    if not os.path.exists(abs_file_path) or not os.path.isfile(abs_file_path):
        print(
            f'Error: File not found or is not a regular file: "{file_path}" is not a file'
        )
        return

    try:
        with open(abs_file_path, "r") as file:
            content = file.read(MAX_CHARS)
            if len(content) == MAX_CHARS:
                content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        print(content)
    except Exception as e:
        print(f"Error: {str(e)}")
        return
