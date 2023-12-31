import os

from tree_dot.models import SkipDirectory, Dot
from tree_dot.views import BaseView, keep, scan, skip
from typing import Callable


ZIP_FOLDER = ".trdt"
OVERVIEW_TITLE = "## Project Overview"
OUTPUT = ZIP_FOLDER + "/.compressed_context"
MD_TITLE = "# Project Overview"
BR = "\n"
BLOCK = "`" + "`" + "`"


def overview_tree(
    dir_filter: SkipDirectory, view: BaseView, directory: str = ".", indent=""
) -> str:
    tree_structure = []
    dir_content = os.listdir(directory)
    for item in dir_content:
        path = os.path.join(directory, item)
        if os.path.isdir(path):
            if not skip(item, dir_filter):
                tree_structure.append(f"{indent}{item}")
                tree_structure.append(
                    overview_tree(
                        dir_filter, view, directory=path, indent=indent + "  "
                    )
                )
        else:
            if keep(item, view, item):
                tree_structure.append(f"{indent}{item}")
    return "\n".join(tree_structure)


def code_block(dot_file: Dot, comment: str | None, title: str = "") -> str:
    with open(dot_file.path) as file:
        content = file.read()

    if comment:
        comment = BR + comment + BR
    else:
        comment, title = "", f"**{dot_file.path.removeprefix('./')}**{BR}"
    block = BLOCK + "{lang}" + "{comment}" + BR + "{content}" + BLOCK
    block = title + block
    return block.format(lang=dot_file.ext, comment=comment, content=content)


def md_report(view_context: Callable, output: str = OUTPUT, root: str = ".") -> str:
    dir_filter, view = view_context()
    paths = scan(root, view, dir_filter)
    ov_tree = overview_tree(dir_filter, view)
    md_blocks = [
        MD_TITLE + BR,
        "#### ROOT FOLDER: " + root,
        OVERVIEW_TITLE + BR + BLOCK + "txt" + BR + ov_tree + BR + BLOCK,
    ]
    for file_path in paths:
        file = keep(file_path.split(os.sep)[-1], view, file_path)
        file.path = file_path
        comment = None
        if file.comment:
            file_path = file_path.removeprefix("./")  # TODO for Windows
            comment = file.comment[0] + file_path + file.comment[1]
        md_blocks.append(code_block(file, comment) + BR)
    if not os.path.exists(ZIP_FOLDER):
        os.mkdir(ZIP_FOLDER)
    if not os.path.exists(output):
        os.mkdir(output)
    md_file = view_context.__name__ + ".md"
    with open(f"{output}/{md_file}", "w") as report_file:
        report_file.write("\n".join(md_blocks))
