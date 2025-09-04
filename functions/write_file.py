def write_file(working_directory, file_path, content):
    import os

    abs_file_path = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, file_path))
    )

    # If the file_path is outside of the working_directory, return a string with an error:
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        print(
            f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        )
        return

    # If the file_path is not a file, return a string with an error:
    if not os.path.exists(os.path.dirname(abs_file_path)):
        print(
            f'Error: Cannot write to "{file_path}" as file path does not exist'
        )
        return

    # Overwrite the contents of the file with the content argument.
    with open(abs_file_path, "w") as f:
        f.write(content)

    print(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')
