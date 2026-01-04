import os


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
