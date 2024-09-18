# Python Standard Library Imports
import pathlib


def is_pathlib_path(path):
    return isinstance(path, type(pathlib.Path()))


def read_file_oneline(file_path):
    if is_pathlib_path(file_path):
        file_path = str(file_path)

    try:
        with open(file_path, 'r') as f:
            return f.readline().strip()
    except Exception as e:
        return f"Error: {str(e)}"
