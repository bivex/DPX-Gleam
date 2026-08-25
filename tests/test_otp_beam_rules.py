"""Unit tests for Gleam OTP and BEAM concurrency rules."""

from __future__ import annotations

from pattern_detector.adapters.outbound.parsers.native_gleam_parser import NativeGleamParserAdapter
from pattern_detector.domain.rules.otp_beam_rules import (
    GleamOtpActorProcessRule,
    ProcessMessagePassingRule,
    SupervisorTreeSpecRule,
    TaskAsyncAwaitRule,
)
from pattern_detector.domain.value_objects import PatternType


def test_gleam_otp_actor_process() -> None:
    code = """
pub fn start_link() {
  actor.start(0, handle_message)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("server.gleam", code)])

    rule = GleamOtpActorProcessRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.GLEAM_OTP_ACTOR_PROCESS


def test_supervisor_tree_spec() -> None:
    code = """
pub fn start_supervisor() {
  supervisor.start(fn(children) {
    children
    |> supervisor.add(supervisor.worker(start_worker))
  })
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("sup.gleam", code)])

    rule = SupervisorTreeSpecRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.SUPERVISOR_TREE_SPEC


def test_process_message_passing() -> None:
    code = """
pub fn send_notification(subject: process.Subject(String), msg: String) {
  process.send(subject, msg)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("msg.gleam", code)])

    rule = ProcessMessagePassingRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.PROCESS_MESSAGE_PASSING


def test_task_async_await() -> None:
    code = """
pub fn fetch_data() {
  let job = task.async(fn() { http.get("https://api.com") })
  task.await(job, 5000)
}
"""
    parser = NativeGleamParserAdapter()
    model = parser.parse_codebase([("task.gleam", code)])

    rule = TaskAsyncAwaitRule()
    detections = rule.evaluate(model)

    assert len(detections) == 1
    assert detections[0].pattern_type == PatternType.TASK_ASYNC_AWAIT
