"""Domain CodeModel entities representing Gleam AST and structural semantics."""

from __future__ import annotations

from dataclasses import dataclass, field
from pattern_detector.domain.value_objects import SourceLocation


@dataclass
class GleamField:
    """Named field in a Gleam record or variant constructor."""

    name: str
    type_name: str
    location: SourceLocation | None = None


@dataclass
class GleamVariant:
    """Variant constructor in a Gleam Custom Type."""

    name: str
    fields: list[GleamField] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class GleamCustomType:
    """Gleam Custom Type (ADT / Sum type / Record)."""

    name: str
    is_pub: bool = False
    is_opaque: bool = False
    type_params: list[str] = field(default_factory=list)
    variants: list[GleamVariant] = field(default_factory=list)
    location: SourceLocation | None = None
    raw_text: str = ""

    @property
    def is_sum_type(self) -> bool:
        return len(self.variants) > 1

    @property
    def total_fields_count(self) -> int:
        return sum(len(v.fields) for v in self.variants)


@dataclass
class GleamParam:
    """Function argument in Gleam."""

    name: str
    type_name: str = "dynamic"


@dataclass
class GleamFunction:
    """Function definition in Gleam ('pub fn' or 'fn')."""

    name: str
    is_pub: bool = False
    parameters: list[GleamParam] = field(default_factory=list)
    return_type: str = "Nil"
    body: str = ""
    pipes_count: int = 0
    cases_count: int = 0
    uses_count: int = 0
    branch_count: int = 1
    has_todo: bool = False
    has_panic: bool = False
    location: SourceLocation | None = None
    raw_text: str = ""

    @property
    def is_actor_loop(self) -> bool:
        return "actor.continue" in self.body or "actor.Stop" in self.body or "loop(" in self.name


@dataclass
class GleamImport:
    """Module import statement in Gleam."""

    module_name: str
    alias: str | None = None
    unqualified_items: list[str] = field(default_factory=list)
    location: SourceLocation | None = None


@dataclass
class GleamFile:
    """Parsed single Gleam source file (.gleam)."""

    file_path: str
    raw_content: str
    lines: list[str] = field(default_factory=list)
    imports: list[GleamImport] = field(default_factory=list)
    types: list[GleamCustomType] = field(default_factory=list)
    functions: list[GleamFunction] = field(default_factory=list)


@dataclass
class CodeModel:
    """Aggregated structural model of a scanned Gleam codebase."""

    target_path: str = ""
    files: list[GleamFile] = field(default_factory=list)

    @property
    def all_types(self) -> list[GleamCustomType]:
        return [t for f in self.files for t in f.types]

    @property
    def all_functions(self) -> list[GleamFunction]:
        return [fn for f in self.files for fn in f.functions]

    @property
    def all_imports(self) -> list[GleamImport]:
        return [imp for f in self.files for imp in f.imports]
