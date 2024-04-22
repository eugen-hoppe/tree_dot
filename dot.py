import os

from datetime import datetime
from typing import TextIO


INCLUDE_EXTENSIONS = []


# Configuration
# =============
ROOT_DIR = "."
OVERVIEW_PATH = ".overview"


# Configuration / Uncomment for Including in Overview Generation
# ==============================================================
INCLUDE_EXTENSIONS += ["Dockerfile"]
# INCLUDE_EXTENSIONS += ["c"]    # C source files
# INCLUDE_EXTENSIONS += ["cpp"]  # C++ source files
# INCLUDE_EXTENSIONS += ["css"]  # Cascading Style Sheets
# INCLUDE_EXTENSIONS += ["csv"]  # Comma-separated values
INCLUDE_EXTENSIONS += ["html"] # HyperText Markup Language
# INCLUDE_EXTENSIONS += ["java"] # Java source files
INCLUDE_EXTENSIONS += ["js"]   # JavaScript
# INCLUDE_EXTENSIONS += ["json"] # JSON data files
INCLUDE_EXTENSIONS += ["py"]   # Python script files
# INCLUDE_EXTENSIONS += ["ts"]   # TypeScript
# INCLUDE_EXTENSIONS += ["txt"]  # Textdateien

# INCLUDE_EXTENSIONS += ["?" ] # Add Custom Extensions


EXCLUDE_DIR_PREFIXES = [
    ".",
    "__",
]
EXCLUDE_FILE_PREFIXES = [
    ".",
    "log_",
    "py_should_excluded",
]


# Overview Generation (Markdown)
# ==============================
MD_TITLE = "Project Overview"
PROJECT_TREE_TITLE = "Project Structure"
CONTENT_SECTION_TITLE = "Content"
CODE_BLOCK_LABELS = {
    "js": "javascript",
    "md": "markdown",
    "php": "php",
    "pl": "perl",
    "ps1": "powershell",
    "py": "python",
    "rb": "ruby",
    "scss": "scss",
    "sh": "bash",
    "sql": "sql",
    "ts": "typescript",
    "yaml": "yaml",
    "yml": "yaml",
    "Dockerfile": "Dockerfile"
}


# Application Constants
# =====================
EXCLUDE_FILE_PREFIXES_INCLUDING_THIS_FILE = [
    os.path.basename(__file__).removesuffix(".py"),
    *EXCLUDE_FILE_PREFIXES
]


def create_project_tree(
    directory: str,
    extensions: str,  # include
    dir_prefixes: list[str],  # exclude
    file_prefixes: list[str]  # exclude
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


def write_tree_to_md(
    dict_item: dict[str | int, str | dict],
    md_file: TextIO,
    indent=''
) -> None:
    for key, value in dict_item.items():
        if isinstance(key, int):
            md_file.write(f"{indent}- {value}\n")
        else:
            md_file.write(f"{indent}- {key}/\n")
            write_tree_to_md(value, md_file, indent + '  ')


def generate_markdown_overview(
    project_dict: dict[str | int, str | dict],
    content_dict: dict[str, str],
    output_path: str | None = None,
    h2: str = "## ",
    br: str ="\n",
    code: str = "```"
) -> None:
    if output_path is None:
        output_path = os.path.join(
            OVERVIEW_PATH, f"{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        )
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as md_file:

        # Project Tree Block
        # ==================
        md_file.write(f"# {MD_TITLE}{br}{br}{h2}{PROJECT_TREE_TITLE}{br}{br}")
        md_file.write(f"{code}txt{br}")
        write_tree_to_md(project_dict, md_file)
        md_file.write(f"{br}{code}{br}")

        # Project View Configuration
        # ==========================
        md_file.write(f"{br}{h2}File and Directories Considerations{br}{br}")
        md_file.write(f"{code}txt{br}")
        md_file.write(
            f"ROOT_DIR: {ROOT_DIR}{br}"
            + f"INCLUDE_EXTENSIONS: ({', '.join(INCLUDE_EXTENSIONS)}){br}"
            + f"EXCLUDE_DIR_PREFIXES: ({', '.join(EXCLUDE_DIR_PREFIXES)}){br}"
            + f"EXCLUDE_FILE_PREFIXES: ({', '.join(EXCLUDE_FILE_PREFIXES)}){br}"
        )
        md_file.write(f"{br}{code}{br}")

        # Content
        # =======
        md_file.write(f"{br}{h2}{CONTENT_SECTION_TITLE}{br}{br}")
        for path, content in content_dict.items():

            # Code Blocks
            # ===========
            extension = path.split(".")[-1]
            code_label = CODE_BLOCK_LABELS.get(extension, extension)
            md_file.write(f"**`{'` / `'.join(path.split('/'))}`**{br}{br}")
            md_file.write(f"{code}{code_label}{br}")
            md_file.write(content)
            md_file.write(f"{br}{code}{br}{br}")


if __name__ == "__main__":
    project_dict = create_project_tree(
        ROOT_DIR,
        INCLUDE_EXTENSIONS,
        EXCLUDE_DIR_PREFIXES,
        EXCLUDE_FILE_PREFIXES_INCLUDING_THIS_FILE
    )
    generate_markdown_overview(
        project_dict,
        content_dict=create_content_dict(ROOT_DIR, project_dict)
    )
