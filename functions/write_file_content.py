import os

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
