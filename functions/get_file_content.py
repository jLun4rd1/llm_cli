import os
from config import MAX_CHARS
from google.genai import types


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads a file's content in a specified directory relative to the working directory, returning its contents in a String format",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to be read, relative to the working directory",
            ),
        },
        required=["file_path"]
    ),
)

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
        return f"Error: getting contents from file: {e}"

    return file_content_str
