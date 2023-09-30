from dataclasses import dataclass, field


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
    comment: tuple[str, str] = ("#", "")


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