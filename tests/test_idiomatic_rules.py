"""Unit tests for Gleam Idiomatic and Functional Core rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.idiomatic_rules import (
    CustomTypeAlgebraicDataTypesRule,
    ExhaustivePatternMatchingRule,
    OpaqueTypeEncapsulationRule,
    PipeOperatorFlowRule,
    ResultMonadRailwayRule,
    UseSyntaxContinuationRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_custom_type_algebraic_data_types() -> None:
    code = """
pub type PaymentStatus {
  Pending
  Authorized(tx_id: String)
  Failed(reason: String)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("payment.gleam", code)])

    rule = CustomTypeAlgebraicDataTypesRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.CUSTOM_TYPE_ALGEBRAIC_DATA_TYPES
    assert detections[0].target_name == "PaymentStatus"


def test_exhaustive_pattern_matching() -> None:
    code = """
pub fn handle_status(status: PaymentStatus) -> String {
  case status {
    Pending -> "Waiting"
    Authorized(id) -> "Success: " <> id
    Failed(err) -> "Error: " <> err
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("handler.gleam", code)])

    rule = ExhaustivePatternMatchingRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.EXHAUSTIVE_PATTERN_MATCHING


def test_pipe_operator_flow() -> None:
    code = """
pub fn transform_numbers(numbers: List(Int)) -> List(Int) {
  numbers
  |> list.filter(fn(x) { x > 0 })
  |> list.map(fn(x) { x * 2 })
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("pipe.gleam", code)])

    rule = PipeOperatorFlowRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PIPE_OPERATOR_FLOW


def test_opaque_type_encapsulation() -> None:
    code = """
pub opaque type UserSession {
  UserSession(token: String, user_id: Int)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("session.gleam", code)])

    rule = OpaqueTypeEncapsulationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.OPAQUE_TYPE_ENCAPSULATION
    assert detections[0].target_name == "UserSession"


def test_result_monad_railway() -> None:
    code = """
pub fn parse_user_age(input: String) -> Result(Int, String) {
  int.parse(input)
  |> result.map_error(fn(_) { "Invalid number" })
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("age.gleam", code)])

    rule = ResultMonadRailwayRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.RESULT_MONAD_RAILWAY


def test_use_syntax_continuation() -> None:
    code = """
pub fn process_request(req: Request) -> Response {
  use auth <- require_auth(req)
  use payload <- parse_json(req.body)
  respond_ok(payload)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("req.gleam", code)])

    rule = UseSyntaxContinuationRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.USE_SYNTAX_CONTINUATION
