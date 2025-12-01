import os
from config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads and returns the first {MAX_CHARS} characters of the content from a specified file within the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file whose content should be read, relative to the working directory.",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory,file_path)
        abs_path_wd = os.path.abspath(working_directory)
        abs_path_cd = os.path.abspath(full_path)

        if not abs_path_cd.startswith(abs_path_wd):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(abs_path_cd):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        with open(abs_path_cd,"r") as f:
            file_content_string = f.read(MAX_CHARS)
            if os.path.getsize(abs_path_cd) > MAX_CHARS:
                content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
        return file_content_string
    except Exception as e:
        return f'Error: {e}'