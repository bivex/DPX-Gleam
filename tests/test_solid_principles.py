"""Unit tests for Gleam SOLID principles and clean code quality rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.solid_principles_rules import (
    DeepCaseCascadeOcpRule,
    DemeterLawTrainWreckRule,
    DryDuplicateLogicRule,
    FatModuleInterfaceIspRule,
    KissCyclomaticComplexityRule,
    KissLongParameterListRule,
    MonolithicCustomTypeSrpRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_monolithic_custom_type_srp() -> None:
    fields = ", ".join(f"field_{i}: String" for i in range(12))
    code = f"""
pub type HugeRecord {{
  HugeRecord({fields})
}}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("huge.gleam", code)])

    rule = MonolithicCustomTypeSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.MONOLITHIC_CUSTOM_TYPE_SRP


def test_fat_module_interface_isp() -> None:
    fns = "\n".join(f"pub fn func_{i}() {{ Nil }}" for i in range(14))
    code = f"""
{fns}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("fat_module.gleam", code)])

    rule = FatModuleInterfaceIspRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.FAT_MODULE_INTERFACE_ISP


def test_deep_case_cascade_ocp() -> None:
    branches = "\n".join(f"    Option_{i} -> {i}" for i in range(10))
    code = f"""
pub fn evaluate_options(opt: Option) -> Int {{
  case opt {{
{branches}
  }}
}}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("cascade.gleam", code)])

    rule = DeepCaseCascadeOcpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DEEP_CASE_CASCADE_OCP


def test_kiss_cyclomatic_complexity() -> None:
    branches = "\n".join(f"    Val_{i} -> {i}" for i in range(10))
    code = f"""
pub fn complex_fn(x: Val) -> Int {{
  case x {{
{branches}
  }}
}}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("complex.gleam", code)])

    rule = KissCyclomaticComplexityRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.KISS_CYCLOMATIC_COMPLEXITY


def test_kiss_long_parameter_list() -> None:
    code = """
pub fn massive_args(a: Int, b: Int, c: Int, d: Int, e: Int, f: Int, g: Int) {
  Nil
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("args.gleam", code)])

    rule = KissLongParameterListRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.KISS_LONG_PARAMETER_LIST


def test_dry_duplicate_logic() -> None:
    body = "let x = 10 + 20\n  let y = x * 30\n  let z = y / 2\n  z"
    code = f"""
pub fn calc_a() {{
  {body}
}}

pub fn calc_b() {{
  {body}
}}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("dry.gleam", code)])

    rule = DryDuplicateLogicRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DRY_DUPLICATE_LOGIC


def test_demeter_law_train_wreck() -> None:
    code = """
pub fn get_user_city(user: User) {
  user.profile.contact.address.city
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("demeter.gleam", code)])

    rule = DemeterLawTrainWreckRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.DEMETER_LAW_TRAIN_WRECK
