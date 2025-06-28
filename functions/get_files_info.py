def get_files_info(working_directory, directory=None):
    if directory is None:
        directory = working_directory

    if not directory.startswith(working_directory):
        raise ValueError(
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        )

    if not os.path.exists(directory):
        raise ValueError(f'Error: Directory "{directory}" does not exist')

    if not os.path.isdir(directory):
        raise ValueError(f'Error: "{directory}" is not a directory')

    import os

    files_info = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            file_path = os.path.join(root, filename)
            file_info = {
                "name": filename,
                "path": file_path,
                "size": os.path.getsize(file_path),
                "modified": os.path.getmtime(file_path),
            }
            files_info.append(file_info)

    return files_info
