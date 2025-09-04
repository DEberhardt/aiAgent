def run_python_file(working_directory, file_path, args=[]):
    import os
    import subprocess

    abs_file_path = os.path.normpath(
        os.path.abspath(os.path.join(working_directory, file_path))
    )

    # If the file_path is outside of the working_directory, return a string with an error:
    abs_working_directory = os.path.abspath(working_directory)
    if not abs_file_path.startswith(abs_working_directory):
        print(
            f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        )
        return

    # If the file does not exist, return a string with an error:
    if not os.path.isfile(abs_file_path):
        print(f'Error: File "{file_path}" not found')
        return

    # If the file does not end in .py, return a string with an error:
    if not abs_file_path.endswith(".py"):
        print(f'Error: File "{file_path}" is not a Python file')
        return

    # Run the Python file with the provided arguments
    #
    # Set a timeout of 30 seconds to prevent infinite execution
    # Capture both stdout and stderr
    # Set the working directory properly
    # Pass along the additional args if provided
    #
    # If the process exits with a non-zero code, include "Process exited with code X"
    # If no output is produced, return "No output produced."
    try:
        result = subprocess.run(
            ["python", abs_file_path] + args,
            capture_output=True,
            text=True,
            check=True,
            cwd=abs_working_directory,
            timeout=30
        )
        if result.stdout.strip() == "":
            print("No output produced.")
        else:
            print(f'STDOUT::"{file_path}":')
            print(result.stdout)
        if result.stderr.strip() != "":
            print(f'STDERR:"{file_path}": {result.stderr}')
    except subprocess.CalledProcessError as e:
        print(f'STDERR:"{file_path}": {e.stderr}')
        print(f'Process exited with code {e.returncode}')
        return
    except subprocess.TimeoutExpired:
        print(f'Error: Process for "{file_path}" timed out after 30 seconds')
        return
    except Exception as e:
        # print(f'Error: An unexpected error occurred while running "{file_path}": {str(e)}')
        print(f"Error: executing Python file: {e}")
        return
