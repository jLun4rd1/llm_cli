import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_abs_path, file_path))
        valid_target_file = os.path.commonpath([wd_abs_path, target_file]) == wd_abs_path
        if not valid_target_file:
            return f'    Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'    Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            if f.read(1):
                truncate_message = f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                print(f"Inserting truncate message of length {len(truncate_message)}...")
                file_content_str += truncate_message

    except Exception as e:
        return f"Error: {e}"

    return file_content_str
