"""Unit tests for Gleam functional composition and updates."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.functional_rules import (
    CurryingPartialApplicationRule,
    HigherOrderFunctionPipelineRule,
    PureRecordUpdateSyntaxRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_higher_order_function_pipeline() -> None:
    code = """
pub fn sum_evens(nums: List(Int)) -> Int {
  nums
  |> list.filter(fn(x) { x % 2 == 0 })
  |> list.fold(0, fn(acc, x) { acc + x })
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("hof.gleam", code)])

    rule = HigherOrderFunctionPipelineRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.HIGHER_ORDER_FUNCTION_PIPELINE


def test_currying_partial_application() -> None:
    code = """
pub fn make_adder(x: Int) {
  fn(y: Int) {
    fn(z: Int) { x + y + z }
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("curry.gleam", code)])

    rule = CurryingPartialApplicationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CURRYING_PARTIAL_APPLICATION


def test_pure_record_update_syntax() -> None:
    code = """
pub fn update_user_email(user: User, new_email: String) -> User {
  User(..user, email: new_email)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("update.gleam", code)])

    rule = PureRecordUpdateSyntaxRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PURE_RECORD_UPDATE_SYNTAX
