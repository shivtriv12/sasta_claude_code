import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run the specified python file given in the file_path with optional arguments, constrained to the working directory.Also returns the output from the interpreter.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file which is to run, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Optional arguments to pass to the Python file.",
                ),
                description="Optional list of arguments which may be required during running certain files.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory,file_path)
        abs_path_wd = os.path.abspath(working_directory)
        abs_path_cd = os.path.abspath(full_path)

        if not abs_path_cd.startswith(abs_path_wd):
            return f'Error: Cannot execute "{file_path}" as it is outside'
        if not os.path.exists(abs_path_cd):
            return f'Error: File "{file_path}" not found.'
        if not abs_path_cd.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'
        
        commands = ["python", abs_path_cd]
        if args:
            commands.extend(args)
        result = subprocess.run(
            commands,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=abs_path_wd,
        )
        output = []
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")

        return "\n".join(output) if output else "No output produced."
    except Exception as e:
        return f'Error: {e}'