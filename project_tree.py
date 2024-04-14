import os
from pprint import pprint


ROOT_DIR = "sandbox"
EXTENSIONS = [
    "py",
    "html",
    "txt",
]
DIR_PREFIXES = [
    ".",
    "__",
]
FILE_PREFIXES = [
    os.path.basename(__file__).removesuffix(".py"),  # this file
    ".",
    "log_",
]


def create_project_tree(
    directory: str,
    extensions: str,
    dir_prefixes: list[str],
    file_prefixes: list[str]
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
            if path.split(".")[-1] in extensions:
                result[file_count] = item
                file_count += 1
    return result


def read_files_to_dict(
    directory: str,
    file_dict: dict[str | int, str | dict],
    result: dict[str, str]
) -> None:
    for key, value in file_dict.items():
        if isinstance(key, int):
            file_path = os.path.join(directory, value)
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    result[file_path] = file.read()
            except Exception as e:
                result[file_path] = str(e)
        elif isinstance(value, dict):
            new_directory = os.path.join(directory, key)
            read_files_to_dict(new_directory, value, result)


def create_content_dict(
    root_directory: str,
    project_dict: dict[str | int, str | dict]
) -> dict[str, str]:
    content_dict = {}
    read_files_to_dict(root_directory, project_dict, content_dict)
    return content_dict


if __name__ == "__main__":
    project_dict = create_project_tree(
        ROOT_DIR, EXTENSIONS, DIR_PREFIXES, FILE_PREFIXES
    )
    content_dict = create_content_dict(ROOT_DIR, project_dict)

    pprint(project_dict, indent=4)
    print()
    pprint(content_dict, indent=4)
