import os
import subprocess
from google.genai import types


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in a specified directory relative to the working directory, returning a formatted String that can include: no output at all; standard output; standard error output; exit code in case it's different from 0",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Python file path to be executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of arguments to pass to the Python script",
            ),
        },
        required=["file_path"]
    ),
)

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
