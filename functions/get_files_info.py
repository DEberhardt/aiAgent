def get_files_info(working_directory, directory="."):
    import os

    output_directory = f"'{directory}'"
    if directory == ".":
        output_directory = "current"

    # Convert to absolute paths and normalize
    abs_working_directory = os.path.abspath(working_directory)
    # print(f"Working directory: {abs_working_directory}")

    abs_directory = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, directory))
    )
    # print(f"Child directory:   {abs_directory}")

    # Check if abs_directory is a subdirectory (or same as) abs_working_directory
    if not abs_directory.startswith(abs_working_directory):
        print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        return
    # else:
    #     print("Directory exists within the working directory")

    if not os.path.exists(abs_directory):
        print(f'Error: Directory "{directory}" does not exist')
        return

    if not os.path.isdir(abs_directory):
        print(f'Error: "{directory}" is not a directory')
        return

    files_info = []
    try:
        for entry in os.scandir(abs_directory):
            file_info = f"{entry.name}: file_size={entry.stat().st_size} bytes, is_dir={entry.is_dir()}"
            files_info.append(file_info)
    except Exception as e:
        print(f"Error: {str(e)}")
        return

    print(f"Result for {output_directory} directory:")
    for info in files_info:
        print(f" - {info}")

