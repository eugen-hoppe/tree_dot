import os
from pprint import pprint


ROOT_DIR = "."
EXTENSIONS = ['py', "txt"]
DIR_PREFIXES = ['.', '__']
FILE_PREFIXES = ['.', 'log_', "treedot"]


def create_project_tree(
    directory: str, extensions: str, dir_prefixes: str, file_prefixes: str
) -> dict[str | int, str | dict]:
    result = {}
    dir_content = sorted(os.listdir(directory))

    file_count = 0
    for item in dir_content:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if any(item.startswith(prefix) for prefix in dir_prefixes):
                continue
            result[item] = create_project_tree(
                path, extensions, dir_prefixes, file_prefixes
            )
        elif os.path.isfile(path):
            if any(item.startswith(prefix) for prefix in file_prefixes):
                continue
            if path.split('.')[-1] in extensions:
                result[file_count] = item
                file_count += 1
    return result



project_dict = create_project_tree(
    ROOT_DIR, EXTENSIONS, DIR_PREFIXES, FILE_PREFIXES
)


pprint(project_dict, indent=4)
