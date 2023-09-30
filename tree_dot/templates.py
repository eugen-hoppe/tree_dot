#tree_dot/templates.py

from dataclasses import dataclass, field

import tree_dot.models as m


@dataclass
class Template:
    gitignore: m.Gitignore | None  = field(default_factory=lambda: m.Gitignore())


@dataclass
class Web(Template):
    html: m.HTML | None = field(default_factory=lambda: m.HTML())
    css: m.CSS = field(default_factory=lambda: m.CSS())


@dataclass
class Database(Template):
    sql: m.SQL | None  = field(default_factory=lambda: m.SQL())


@dataclass
class Config(Template):
    json: m.JSON | None  = field(default_factory=lambda: m.JSON())


@dataclass
class Docker(Template):
    dockerfile: m.Dockerfile | None  = field(default_factory=lambda: m.Dockerfile())
    docker_compose: m.DockerCompose | None  = field(
        default_factory=lambda: m.DockerCompose()
    )


@dataclass
class Python(Template):
    py: m.PY | None  = field(default_factory=lambda: m.PY())
    env: m.ENV | None  = field(default_factory=lambda: m.ENV())
    txt_requirements: m.TXTRequirements | None  = field(
        default_factory=lambda: m.TXTRequirements()
    )


@dataclass
class JavaScript(Template):
    js: m.TSX | None = field(default_factory=lambda: m.JS())
    tsx: m.TSX | None = field(default_factory=lambda: m.TSX())
    ts: m.TSX | None = field(default_factory=lambda: m.TSX())

