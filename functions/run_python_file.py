import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    try:
        wd_abs_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(wd_abs_path, file_path))

        valid_target_file = os.path.commonpath([wd_abs_path, target_file]) == wd_abs_path
        if not valid_target_file:
            return f'    Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'    Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'    Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=wd_abs_path,
            capture_output=True,
            text=True,
            timeout=30
        )

        final_return_message = []
        if result.returncode != 0:
            final_return_message.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            final_return_message.append(f"No output produced")
        if result.stdout:
            final_return_message.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            final_return_message.append(f"STDERR:\n{result.stderr}")

    except Exception as e:
        return f"Error: executing Python file: {e}"

    return "\n".join(final_return_message)
