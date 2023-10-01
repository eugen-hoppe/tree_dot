from tree_dot.models import SkipDirectory
from tree_dot.report import md_report
from tree_dot.views import BaseView

# 01.10.2023
# ==========


def fast_api_project() -> tuple[SkipDirectory, BaseView]:
    skip_dir = SkipDirectory()
    skip_dir.names = ["venv", "tree_dot"]
    skip_dir.if_starts_with = [".", "_", "test_"]
    view = BaseView()

    view.py.keep = True
    view.html.keep = True
    view.dockerfile.keep = True
    view.txt_requirements.keep = True

    return skip_dir, view


def react_native() -> tuple[SkipDirectory, BaseView]:
    skip_dir = SkipDirectory()
    skip_dir.names = ["assets", "config"]
    skip_dir.if_starts_with = [".", "_"]

    view = BaseView()
    view.tsx.keep = True
    view.ts.keep = True
    view.js.keep = True

    return skip_dir, view


if __name__ == "__main__":
    context_reports = [fast_api_project, react_native]
    for func in context_reports:
        md_report(view_context=func)
