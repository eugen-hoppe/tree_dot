from tree_dot.models import SkipDirectory
from tree_dot.report import md_report
from tree_dot.views import BaseView


DIRECTORY = "./sandbox"  # DIRECTORY = "."
SKIP_DIR = SkipDirectory(
    names=["tree_dot", "installation", "trdt"],
    if_starts_with=[".", "_"]
)


def fast_api_project(skip_dir: SkipDirectory = SKIP_DIR) -> tuple[SkipDirectory, BaseView]:
    skip_dir.names += ["venv"]
    skip_dir.if_starts_with += ["test_"]
    view = BaseView()

    view.py.keep = True
    view.html.keep = True
    view.dockerfile.keep = True
    view.txt_requirements.keep = True

    return skip_dir, view


def react_native(skip_dir: SkipDirectory = SKIP_DIR) -> tuple[SkipDirectory, BaseView]:
    skip_dir.names += ["assets", "config"]
    skip_dir.if_starts_with += []

    view = BaseView()
    view.tsx.keep = True
    view.ts.keep = True
    view.js.keep = True

    return skip_dir, view


if __name__ == "__main__":
    context_reports = [
        fast_api_project,
        react_native
    ]
    for func in context_reports:
        md_report(view_context=func, root=DIRECTORY)
