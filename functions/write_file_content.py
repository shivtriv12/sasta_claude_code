import os
from google import genai
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write the content specified to a file_path specified,if file does not exist create it, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to write/modify to, realtive to working directory. If path does not already exists create it.",
            ),
            "content":types.Schema(
                type=types.Type.STRING,
                description="Content to write to file_path.",
            )
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory,file_path,content):
    try:
        full_path = os.path.join(working_directory,file_path)
        abs_path_wd = os.path.abspath(working_directory)
        abs_path_cd = os.path.abspath(full_path)

        if not abs_path_cd.startswith(abs_path_wd):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.exists(abs_path_cd):
            os.makedirs(os.path.dirname(abs_path_cd),exist_ok=True)
        if os.path.exists(abs_path_cd) and os.path.isdir(abs_path_cd):
            return f'Error: "{file_path}" is a directory, not a file'
        
        with open(full_path,"w") as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'
