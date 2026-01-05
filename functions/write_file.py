import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the contents of a file in a specified directory relative to the working directory, returning a String that reports the success of that action, followed by the amount of characters written, or the failure, represented by an Error of some sort",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to be overwritten, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="Content that will be used to overwrite the file",
            ),
        },
        required=["file_path", "content"]
    ),
)

def write_file(working_directory, file_path, content):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_abs_path, file_path))

        valid_target_file = os.path.commonpath([wd_abs_path, target_file]) == wd_abs_path
        if not valid_target_file:
            return f'    Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'    Error: Cannot write to "{file_path}" as it is a directory'

        print(f"Ensuring existance of parent files: {target_file.split(file_path)[0]} ...")
        os.makedirs(target_file.split(file_path)[0], exist_ok=True)

        with open(target_file, "w") as f:
            f.write(content)

    except Exception as e:
        return f"Error: writing to file: {e}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
