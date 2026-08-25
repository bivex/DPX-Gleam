"""Unit tests verifying zero false positives on clean, idiomatic Gleam code."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules import get_default_rules
from pattern_detector.domain.rules.resilience_hazards_rules import (
    InfiniteActorLoopRule,
    TodoPanicInProductionRule,
    UnhandledResultErrorRule,
)
from pattern_detector.domain.rules.solid_principles_rules import (
    DeepCaseCascadeOcpRule,
    FatModuleInterfaceIspRule,
    KissCyclomaticComplexityRule,
    MonolithicCustomTypeSrpRule,
)
from pattern_detector.domain.services.rule_engine import RuleEngineService
from pattern_detector.domain.value_objects import PatternCategory


def test_clean_actor_loop_with_stop() -> None:
    code = """
pub fn loop(msg: Msg, state: State) {
  case msg {
    Shutdown -> actor.Stop(process.Normal)
    Work(data) -> {
      let next_state = process_data(state, data)
      actor.continue(next_state)
    }
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("clean_actor.gleam", code)])

    rule = InfiniteActorLoopRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_production_code_no_panics() -> None:
    code = """
pub fn safe_divide(a: Int, b: Int) -> Result(Int, String) {
  case b {
    0 -> Error("Cannot divide by zero")
    _ -> Ok(a / b)
  }
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("safe.gleam", code)])

    rule = TodoPanicInProductionRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_cohesive_type_no_monolithic_srp() -> None:
    code = """
pub type User {
  User(id: Int, name: String, email: String)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("user.gleam", code)])

    rule = MonolithicCustomTypeSrpRule()
    detections = rule.evaluate(model)

    assert len(detections) == 0


def test_clean_domain_service_no_hazards() -> None:
    code = """
pub fn calculate_total(items: List(Item)) -> Int {
  items
  |> list.map(fn(i) { i.price * i.quantity })
  |> int.sum
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("calc.gleam", code)])

    engine = RuleEngineService(rules=get_default_rules())
    detections = engine.evaluate(model)

    hazards = [d for d in detections if d.pattern_category in (PatternCategory.RESILIENCE, PatternCategory.PRINCIPLE)]
    assert len(hazards) == 0
