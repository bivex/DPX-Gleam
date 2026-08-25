"""High-speed native parser adapter for Gleam source code (.gleam)."""

from __future__ import annotations

import re
from pattern_detector.domain.code_model import (
    CodeModel,
    GleamCustomType,
    GleamField,
    GleamFile,
    GleamFunction,
    GleamImport,
    GleamParam,
    GleamVariant,
)
from pattern_detector.domain.value_objects import SourceLocation
from pattern_detector.ports.outbound import ParserPort


def _split_top_level_commas(s: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for char in s:
        if char in "([{":
            depth += 1
            current.append(char)
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            parts.append("".join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        parts.append("".join(current).strip())
    return [p for p in parts if p]


class NativeGleamParserAdapter(ParserPort):
    """Single-pass robust parser extracting Gleam AST semantics and custom types."""

    IMPORT_PATTERN = re.compile(
        r"^\s*import\s+(?P<module>[a-zA-Z0-9_/]+)(?:\s+as\s+(?P<alias>[a-zA-Z0-9_]+))?(?:\.\{(?P<unqualified>[^}]+)\})?"
    )
    TYPE_HEADER = re.compile(
        r"^\s*(?P<pub>pub\s+)?(?P<opaque>opaque\s+)?type\s+(?P<name>[a-zA-Z0-9_]+)(?:\((?P<params>[^)]+)\))?\s*(?:\{|\=)?"
    )
    FN_PREFIX_PATTERN = re.compile(r"^\s*(?P<pub>pub\s+)?fn\s+(?P<name>[a-zA-Z0-9_]+)\s*\(")
    VARIANT_PATTERN = re.compile(r"^\s*(?P<name>[A-Z][a-zA-Z0-9_]*)(?:\((?P<fields>.*)\))?")
    BRANCH_KEYWORDS = re.compile(r"->|\bcase\s+|\bbool\.guard\b|&&|\|\|")

    def _parse_params(self, params_str: str) -> list[GleamParam]:
        if not params_str.strip():
            return []

        params: list[GleamParam] = []
        for p_clean in _split_top_level_commas(params_str):
            if ":" in p_clean:
                p_name, p_type = p_clean.split(":", 1)
                params.append(GleamParam(name=p_name.strip(), type_name=p_type.strip()))
            else:
                params.append(GleamParam(name=p_clean, type_name="dynamic"))
        return params

    def _parse_fields(self, fields_str: str) -> list[GleamField]:
        if not fields_str or not fields_str.strip():
            return []

        fields: list[GleamField] = []
        for f_clean in _split_top_level_commas(fields_str):
            if ":" in f_clean:
                f_name, f_type = f_clean.split(":", 1)
                fields.append(GleamField(name=f_name.strip(), type_name=f_type.strip()))
            else:
                fields.append(GleamField(name=f_clean, type_name=f_clean))
        return fields

    def parse_file(self, file_path: str, content: str) -> GleamFile:
        lines = content.splitlines()
        file_obj = GleamFile(file_path=file_path, raw_content=content, lines=lines)

        current_type: GleamCustomType | None = None
        current_function: GleamFunction | None = None
        current_func_body: list[str] = []
        brace_depth = 0

        for line_idx, raw_line in enumerate(lines, 1):
            trimmed = raw_line.strip()

            # Skip comments and empty lines
            if trimmed.startswith("//") or not trimmed:
                continue

            # Imports
            imp_m = self.IMPORT_PATTERN.match(trimmed)
            if imp_m:
                unq_str = imp_m.group("unqualified") or ""
                unq_items = [u.strip() for u in unq_str.split(",") if u.strip()]
                file_obj.imports.append(
                    GleamImport(
                        module_name=imp_m.group("module"),
                        alias=imp_m.group("alias"),
                        unqualified_items=unq_items,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    )
                )
                continue

            # Custom Type Start
            type_m = self.TYPE_HEADER.match(trimmed)
            if type_m and not current_function and not current_type:
                name = type_m.group("name")
                is_pub = bool(type_m.group("pub"))
                is_opaque = bool(type_m.group("opaque"))
                params_str = type_m.group("params") or ""
                type_params = [p.strip() for p in params_str.split(",") if p.strip()]

                current_type = GleamCustomType(
                    name=name,
                    is_pub=is_pub,
                    is_opaque=is_opaque,
                    type_params=type_params,
                    location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                    raw_text=raw_line,
                )

                if "{" in trimmed and "}" in trimmed:
                    inside = trimmed[trimmed.find("{") + 1 : trimmed.rfind("}")].strip()
                    if inside:
                        var_m = self.VARIANT_PATTERN.match(inside)
                        if var_m:
                            v_name = var_m.group("name")
                            f_str = var_m.group("fields") or ""
                            fields = self._parse_fields(f_str)
                            current_type.variants.append(
                                GleamVariant(
                                    name=v_name,
                                    fields=fields,
                                    location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                                )
                            )
                    file_obj.types.append(current_type)
                    current_type = None
                    continue

                if "{" not in trimmed and "=" not in trimmed:
                    file_obj.types.append(current_type)
                    current_type = None
                continue

            # Inside Custom Type: parse variants
            if current_type and not current_function:
                if trimmed == "}":
                    file_obj.types.append(current_type)
                    current_type = None
                    continue

                var_m = self.VARIANT_PATTERN.match(trimmed)
                if var_m:
                    v_name = var_m.group("name")
                    f_str = var_m.group("fields") or ""
                    fields = self._parse_fields(f_str)
                    current_type.variants.append(
                        GleamVariant(
                            name=v_name,
                            fields=fields,
                            location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                        )
                    )
                    if "}" in trimmed:
                        file_obj.types.append(current_type)
                        current_type = None
                    continue

            # Function Start (using balanced parenthesis parsing)
            if not current_function:
                fn_match = self.FN_PREFIX_PATTERN.match(trimmed)
                if fn_match:
                    is_pub = bool(fn_match.group("pub"))
                    fn_name = fn_match.group("name")
                    rest = trimmed[fn_match.end():]
                    
                    depth = 1
                    i = 0
                    while i < len(rest) and depth > 0:
                        if rest[i] == "(":
                            depth += 1
                        elif rest[i] == ")":
                            depth -= 1
                        i += 1
                    
                    params_str = rest[:i-1] if i > 0 else ""
                    after_paren = rest[i:].strip()
                    ret_type = "Nil"
                    if after_paren.startswith("->"):
                        after_paren = after_paren[2:].strip()
                        ret_type = after_paren.rstrip("{").strip() or "Nil"

                    params = self._parse_params(params_str)
                    current_function = GleamFunction(
                        name=fn_name,
                        is_pub=is_pub,
                        parameters=params,
                        return_type=ret_type,
                        location=SourceLocation(file_path=file_path, line=line_idx, column=1),
                        raw_text=raw_line,
                    )
                    current_func_body = [raw_line]
                    brace_depth = raw_line.count("{") - raw_line.count("}")
                    if brace_depth <= 0 and "{" in raw_line:
                        current_function.body = "\n".join(current_func_body)
                        file_obj.functions.append(current_function)
                        current_function = None
                        current_func_body = []
                    continue

            # Accumulate Function Body
            if current_function:
                current_func_body.append(raw_line)
                brace_depth += raw_line.count("{") - raw_line.count("}")
                current_function.pipes_count += raw_line.count("|>")
                current_function.cases_count += raw_line.count("case ")
                if "use " in raw_line and "<-" in raw_line:
                    current_function.uses_count += 1
                current_function.branch_count += len(self.BRANCH_KEYWORDS.findall(raw_line))
                if re.search(r"\btodo\b", raw_line):
                    current_function.has_todo = True
                if re.search(r"\bpanic\b", raw_line):
                    current_function.has_panic = True

                if brace_depth <= 0:
                    current_function.body = "\n".join(current_func_body)
                    file_obj.functions.append(current_function)
                    current_function = None
                    current_func_body = []
                    brace_depth = 0

        # Flush if unclosed at EOF
        if current_type:
            file_obj.types.append(current_type)
        if current_function:
            current_function.body = "\n".join(current_func_body)
            file_obj.functions.append(current_function)

        return file_obj

    def parse_codebase(self, files: list[tuple[str, str]], target_path: str = "") -> CodeModel:
        model = CodeModel(target_path=target_path)
        for fpath, content in files:
            gleam_file = self.parse_file(fpath, content)
            model.files.append(gleam_file)
        return model
