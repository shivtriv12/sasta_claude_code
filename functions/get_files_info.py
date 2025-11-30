import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

def get_files_info(working_directory="calculator",directory="."):
    try:
        full_path = os.path.join(working_directory,directory)
        abs_path_wd = os.path.abspath(working_directory)
        abs_path_cd = os.path.abspath(full_path)

        if not abs_path_cd.startswith(abs_path_wd):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
        
        contents = os.listdir(abs_path_cd)
        files_info=""
        for content in contents:
            filepath = os.path.join(abs_path_cd,content)
            temp = f'- {content}: file_size={os.path.getsize(filepath)} bytes, is_dir={os.path.isdir(filepath)}\n'
            files_info = files_info + temp
        return files_info 
        
    except Exception as e:
        return f'Error: {e}'