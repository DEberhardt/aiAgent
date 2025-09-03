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


from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Retrieves the content of a specific file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to retrieve content from, relative to the working directory.",
            ),
            "file_name": types.Schema(
                type=types.Type.STRING,
                description="The name of the file to retrieve content from.",
            ),
        },
    ),
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes or overwrites content to a specified file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Arguments to pass to the Python script.",
                ),
            ),
        },
    ),
)
