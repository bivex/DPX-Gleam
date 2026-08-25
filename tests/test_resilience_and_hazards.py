"""Unit tests for Gleam Resilience, Safety, and Error Handling hazards."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.resilience_hazards_rules import (
    InfiniteActorLoopRule,
    SwallowedProcessTimeoutRule,
    TodoPanicInProductionRule,
    UnhandledResultErrorRule,
    UntypedDynamicDecodeHazardRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_unhandled_result_error() -> None:
    code = """
pub fn drop_result() {
  let _ = save_to_db(user)
  Nil
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("drop.gleam", code)])

    rule = UnhandledResultErrorRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.UNHANDLED_RESULT_ERROR


def test_infinite_actor_loop() -> None:
    code = """
pub fn loop(msg: Msg, state: State) {
  actor.continue(state)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("loop.gleam", code)])

    rule = InfiniteActorLoopRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.INFINITE_ACTOR_LOOP


def test_todo_panic_in_production() -> None:
    code = """
pub fn critical_feature() {
  panic as "Not implemented yet"
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("panic.gleam", code)])

    rule = TodoPanicInProductionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TODO_PANIC_IN_PRODUCTION


def test_untyped_dynamic_decode_hazard() -> None:
    code = """
pub fn unsafe_convert(raw: Dynamic) {
  dynamic.unsafe_coerce(raw)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("decode.gleam", code)])

    rule = UntypedDynamicDecodeHazardRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.UNTYPED_DYNAMIC_DECODE_HAZARD


def test_swallowed_process_timeout() -> None:
    code = """
pub fn wait_message(subj: process.Subject(Int)) {
  case process.receive(subj, 1000) {
    Ok(val) -> val
    Error(_) -> Nil
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("timeout.gleam", code)])

    rule = SwallowedProcessTimeoutRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SWALLOWED_PROCESS_TIMEOUT
