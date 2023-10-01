# 2023 09 30
import os
from dataclasses import dataclass, field
from typing import Callable


# models.py
# =========
@dataclass
class SkipDirectory:
    names: list[str] = field(default_factory=lambda: [])
    if_starts_with: list[str] = field(default_factory=lambda: [])


@dataclass
class Dot:
    ext: str = ""
    lang: str | None = None
    comment: tuple[str, str] | None = None
    dot: str = "."
    prefix: str = ""
    keep: bool = False
    path: str | None = None

    def __post_init__(self):
        if self.lang is None:
            self.lang = self.ext

    def dot_ext(self) -> str:
        return self.dot + self.ext

    def name(self, core: str = "") -> str:
        return self.prefix + core + self.dot_ext()


@dataclass
class DotHash(Dot):
    comment: tuple[str, str] = ("# ", "")


@dataclass
class DotSlash(Dot):
    comment: tuple[str, str] = ("// ", "")


@dataclass
class Dotless(DotHash):
    dot: str = ""


@dataclass
class Gitignore(DotHash):
    ext: str = "gitignore"


@dataclass
class SQL(Dot):
    ext: str = "sql"
    comment: tuple[str, str] = ("-- ", "")


@dataclass
class SQLITE(Dot):
    ext: str = "sqlite"


@dataclass
class YML(DotHash):
    ext: str = "yml"


@dataclass
class Dockerfile(Dotless):
    ext: str = "Dockerfile"


@dataclass
class DockerCompose(YML):
    prefix: str = "docker-compose"


@dataclass
class HTML(Dot):
    ext: str = "html"
    comment: tuple[str, str] = ("<!-- ", " -->")


@dataclass
class CSS(Dot):
    ext: str = "css"
    comment: tuple[str, str] = ("/* ", " */")


@dataclass
class JSON(Dot):
    ext: str = "json"


@dataclass
class TXT(Dot):
    ext: str = "txt"


@dataclass
class ENV(DotHash):
    ext: str = "env"


@dataclass
class PY(DotHash):
    ext: str = "py"
    lang: str = "python"


@dataclass
class TXTRequirements(TXT):
    prefix: str = "requirements"
    comment: tuple[str, str] = ("# ", "")


@dataclass
class JS(DotSlash):
    ext: str = "js"


@dataclass
class TSX(DotSlash):
    ext: str = "tsx"


@dataclass
class TS(DotSlash):
    ext: str = "ts"


# templates.py
# ============
@dataclass
class Template:
    gitignore: Gitignore | None = field(default_factory=lambda: Gitignore())


@dataclass
class Web(Template):
    html: HTML | None = field(default_factory=lambda: HTML())
    css: CSS = field(default_factory=lambda: CSS())


@dataclass
class Database(Template):
    sql: SQL | None = field(default_factory=lambda: SQL())


@dataclass
class Config(Template):
    json: JSON | None = field(default_factory=lambda: JSON())


@dataclass
class Docker(Template):
    dockerfile: Dockerfile | None = field(default_factory=lambda: Dockerfile())
    docker_compose: DockerCompose | None = field(
        default_factory=lambda: DockerCompose()
    )


@dataclass
class Python(Template):
    py: PY | None = field(default_factory=lambda: PY())
    env: ENV | None = field(default_factory=lambda: ENV())
    txt_requirements: TXTRequirements | None = field(
        default_factory=lambda: TXTRequirements()
    )


@dataclass
class JavaScript(Template):
    js: TSX | None = field(default_factory=lambda: JS())
    tsx: TSX | None = field(default_factory=lambda: TSX())
    ts: TSX | None = field(default_factory=lambda: TSX())


# views.py
# ========
@dataclass
class BaseView(Web, Database, Docker, Python, Config, JavaScript):
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
        skip_ = False
        for root_prefix in skip_roots:
            if root.startswith(root_prefix):
                skip_ = True
                break
        if skip_:
            continue
        for filename in filenames:
            if keep(filename, view):
                paths.append(os.path.join(root, filename))
    return paths


# report.py
# =========
OUTPUT = ".compressed_context"
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
                tree_structure.append(overview_tree(path, indent + "  "))
        else:
            if keep(item, view):
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


def md_report(view_context: Callable, output: str = OUTPUT) -> str:
    dir_filter, view = view_context()
    paths = scan(".", view, dir_filter)
    md_blocks = [MD_TITLE + BR]
    for file_path in paths:
        file = keep(file_path.split("/")[-1], view)
        file.path = file_path
        comment = None
        if file.comment:
            comment = file.comment[0] + file_path.removeprefix("./") + file.comment[1]
        md_blocks.append(code_block(file, comment) + BR)
    if not os.path.exists(output):
        os.mkdir(output)
    md_file = view_context.__name__ + ".md"
    with open(f"{output}/{md_file}", "w") as report_file:
        report_file.write("\n".join(md_blocks))


# dot.py
# ======
def fast_api_project() -> tuple[SkipDirectory, BaseView]:
    skip_dir = SkipDirectory()
    skip_dir.names = ["__pycache__", ".git", ".venv", "venv", "tree_do", "sandbox"]
    skip_dir.if_starts_with = [".", "_", "test_"]
    view = BaseView()

    view.py.keep = True
    view.html.keep = True
    view.dockerfile.keep = True
    view.txt_requirements.keep = True

    return skip_dir, view


def react_native() -> tuple[SkipDirectory, BaseView]:
    skip_dir = SkipDirectory()
    skip_dir.names = ["assets", "config", "constants"]
    skip_dir.if_starts_with = [".", "_", "test_"]

    view = BaseView()
    view.tsx.keep = True
    view.ts.keep = True
    view.js.keep = True

    return skip_dir, view


if __name__ == "__main__":
    context_reports = [fast_api_project, react_native]
    for func in context_reports:
        md_report(view_context=func)
