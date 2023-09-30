import os
from dataclasses import dataclass

from tree_dot import templates
from tree_dot.models import Dot, SkipDirectory


@dataclass
class BaseView(
        templates.Web,
        templates.Database,
        templates.Docker,
        templates.Python,
        templates.Config
        ):
    pass


def skip(directory: str, skip_directory: SkipDirectory) -> bool:
    for skip_dir in skip_directory.if_starts_with:
        if directory.startswith(skip_dir):
            return True
    for skip_dir in skip_directory.names:
        if skip_dir == directory:
            return True
    return False


def keep(filename: str, view: BaseView) -> Dot | None:
    core, *_ = filename.split(".")
    ext = core
    if len(filename.split(".")) > 1:
        _, ext, *_ = filename.split(".")
    for attr in dir(view):
        if attr.startswith("_"):
            continue
        if getattr(view, attr, False):
            file: Dot = getattr(view, attr)
            if ext == file.ext:
                if file.keep:
                    return file
    return None


def scan(path: str, view: BaseView, dir_filter: SkipDirectory) -> list[str]:
    paths = []
    skip_roots = []
    for root, directories, filenames in os.walk(path):
        for directory in directories:
            if skip(directory, dir_filter):
                skip_roots.append(os.path.join(root, directory))
    for root, directories, filenames in os.walk(path):
        if root in skip_roots:
            continue
        for filename in filenames:
            if keep(filename, view):
                paths.append(os.path.join(root, filename))
    return paths
